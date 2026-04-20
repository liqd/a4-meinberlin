from django.contrib import admin
from django.contrib import messages
from django.contrib.gis.admin import GISModelAdmin
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
    from meinberlin.apps.notifications import emails as notification_emails

    sent = 0
    skipped_type = 0
    skipped_draft = 0
    for project in queryset:
        if project.project_type != "a4projects.Project":
            skipped_type += 1
            continue
        if project.is_draft:
            skipped_draft += 1
            continue
        notification_emails.NotifyInitiatorsPublishResultsEmail.send(project)
        sent += 1

    if sent:
        modeladmin.message_user(
            request,
            ngettext(
                "Publish-results reminder sent for %(count)d project "
                "(one e-mail per initiator of the organisation).",
                "Publish-results reminder sent for %(count)d projects "
                "(one e-mail per initiator of each organisation).",
                sent,
            )
            % {"count": sent},
            messages.SUCCESS,
        )
    if skipped_type:
        modeladmin.message_user(
            request,
            ngettext(
                "Skipped %(count)d project (not a standard project).",
                "Skipped %(count)d projects (not standard projects).",
                skipped_type,
            )
            % {"count": skipped_type},
            messages.WARNING,
        )
    if skipped_draft:
        modeladmin.message_user(
            request,
            ngettext(
                "Skipped %(count)d draft project (publish first, or use "
                "manage.py send_publish_results_reminder SLUG --force).",
                "Skipped %(count)d draft projects (publish first, or use "
                "manage.py send_publish_results_reminder SLUG --force).",
                skipped_draft,
            )
            % {"count": skipped_draft},
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
