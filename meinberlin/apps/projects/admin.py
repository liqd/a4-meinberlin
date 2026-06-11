from collections import Counter

from django.contrib import admin
from django.contrib import messages
from django.contrib.gis.admin import GISModelAdmin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from adhocracy4.projects import models
from adhocracy4.projects.admin import ProjectAdminForm


@admin.action(description=_("archive"))
def set_is_archived_true(modeladmin, request, queryset):
    queryset.update(is_archived=True)


@admin.action(description=_("dearchive"))
def set_is_archived_false(modeladmin, request, queryset):
    queryset.update(is_archived=False)


@admin.action(
    description=_("Send publish-results reminder email to initiators"),
)
def send_publish_results_reminder_to_initiators(modeladmin, request, queryset):
    from meinberlin.apps.projects.utils import apply_publish_results_reminder
    from meinberlin.apps.projects.utils import get_publish_results_reminder_skip_reason

    pks = list(queryset.values_list("pk", flat=True))
    projects = (
        models.Project.objects.filter(pk__in=pks)
        .select_related("organisation", "insight")
        .prefetch_related(
            "module_set",
            "module_set__phase_set",
            "organisation__initiators__notification_settings",
        )
    )

    now = timezone.now()
    sent = 0
    skip_reasons: Counter[str] = Counter()

    for project in projects:
        reason = get_publish_results_reminder_skip_reason(project, now=now)
        if reason is not None:
            skip_reasons[reason] += 1
            continue
        apply_publish_results_reminder(project, now=now)
        sent += 1

    if sent:
        modeladmin.message_user(
            request,
            ngettext(
                "Publish-results reminder sent for %(count)d project "
                "(one e-mail per initiator involved in the project).",
                "Publish-results reminder sent for %(count)d projects "
                "(one e-mail per initiator involved in each project).",
                sent,
            )
            % {"count": sent},
            messages.SUCCESS,
        )

    _notify_publish_results_skip_reasons(modeladmin, request, skip_reasons)


def _notify_publish_results_skip_reasons(
    modeladmin, request, skip_reasons: Counter[str]
):
    """Emit one admin message per skip reason (same rules as periodic task)."""
    if not skip_reasons:
        return

    if skip_reasons["project_not_eligible"]:
        n = skip_reasons["project_not_eligible"]
        modeladmin.message_user(
            request,
            ngettext(
                "Skipped %(count)d project (not a standard live project: draft, archived, "
                "or non-default project type).",
                "Skipped %(count)d projects (not standard live projects: draft, archived, "
                "or non-default project type).",
                n,
            )
            % {"count": n},
            messages.WARNING,
        )
    if skip_reasons["reminder_already_sent"]:
        n = skip_reasons["reminder_already_sent"]
        modeladmin.message_user(
            request,
            ngettext(
                "Skipped %(count)d project (publish-results reminder was already sent).",
                "Skipped %(count)d projects (publish-results reminder was already sent).",
                n,
            )
            % {"count": n},
            messages.WARNING,
        )
    if skip_reasons["result_has_content"]:
        n = skip_reasons["result_has_content"]
        modeladmin.message_user(
            request,
            ngettext(
                "Skipped %(count)d project (project results field already has content).",
                "Skipped %(count)d projects (project results field already has content).",
                n,
            )
            % {"count": n},
            messages.WARNING,
        )
    if skip_reasons["reminder_not_due"]:
        n = skip_reasons["reminder_not_due"]
        modeladmin.message_user(
            request,
            ngettext(
                "Skipped %(count)d project (reminder not due yet: participation timing, "
                "minimum last-end cutoff, or delay hours).",
                "Skipped %(count)d projects (reminder not due yet: participation timing, "
                "minimum last-end cutoff, or delay hours).",
                n,
            )
            % {"count": n},
            messages.WARNING,
        )


class ProjectAdmin(GISModelAdmin):
    form = ProjectAdminForm
    list_display = (
        "__str__",
        "slug",
        "organisation",
        "is_draft",
        "is_archived",
        "project_type",
        "created",
    )
    list_filter = ("is_draft", "is_archived", "organisation")
    search_fields = ("name",)
    raw_id_fields = ("moderators", "participants")
    date_hierarchy = "created"
    gis_widget_kwargs = {
        "attrs": {
            "default_zoom": 12,  # Configure zoom level
            "default_lon": 13.404954,
            "default_lat": 52.520008,
        }
    }

    actions = [
        set_is_archived_true,
        set_is_archived_false,
        send_publish_results_reminder_to_initiators,
    ]

    fieldsets = (
        (None, {"fields": ("name", "slug", "organisation", "group")}),
        (
            _("Topic and location"),
            {
                "fields": ("topics", "point", "administrative_district"),
            },
        ),
        (
            _("Information and result"),
            {
                "fields": ("description", "information", "result"),
            },
        ),
        (
            _("Settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "access",
                    "is_draft",
                    "is_archived",
                    "moderators",
                    "participants",
                    "project_type",
                ),
            },
        ),
        (
            _("Images"),
            {
                "classes": ("collapse",),
                "fields": (
                    "image",
                    "image_copyright",
                    "tile_image",
                    "tile_image_alt_text",
                    "tile_image_copyright",
                ),
            },
        ),
        (
            _("Contact"),
            {
                "classes": ("collapse",),
                "fields": (
                    "contact_name",
                    "contact_address_text",
                    "contact_phone",
                    "contact_email",
                    "contact_url",
                ),
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "administrative_district":
            kwargs["empty_label"] = _("City wide")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Overwrite adhocracy4.projects.admin
admin.site.unregister(models.Project)
admin.site.register(models.Project, ProjectAdmin)
