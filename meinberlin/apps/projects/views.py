import itertools

import django_filters
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.views import generic
from rules.contrib.views import LoginRequiredMixin
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.filters import widgets as filters_widgets
from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.filters.filters import DistinctOrderingFilter
from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.filters.widgets import DropdownLinkWidget
from adhocracy4.modules import models as module_models
from adhocracy4.projects import models as project_models
from adhocracy4.projects.mixins import PhaseDispatchMixin
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.offlineevents.models import OfflineEvent

from ..bplan.views import BplanProjectDispatchMixin
from . import forms
from . import models

User = get_user_model()


class OrderingWidget(DropdownLinkWidget):
    label = _("Ordering")
    right = True


class OrganisationWidget(DropdownLinkWidget):
    label = _("Organisation")


class DistrictWidget(DropdownLinkWidget):
    label = _("District")


class FreeTextFilterWidget(filters_widgets.FreeTextFilterWidget):
    label = _("Search")


class ArchivedWidget(DropdownLinkWidget):
    label = _("Archived")

    def __init__(self, attrs=None):
        choices = (
            ("", _("All")),
            ("false", _("No")),
            ("true", _("Yes")),
        )
        super().__init__(attrs, choices)


class YearWidget(DropdownLinkWidget):
    label = _("Year")

    def __init__(self, attrs=None):
        choices = (("", _("Any")),)
        now = timezone.now().year
        try:
            first_year = project_models.Project.objects.earliest("created").created.year
        except project_models.Project.DoesNotExist:
            first_year = now
        for year in range(now, first_year - 1, -1):
            choices += ((year, year),)
        super().__init__(attrs, choices)


class ProjectFilterSet(DefaultsFilterSet):
    defaults = {"is_archived": "false"}

    ordering = DistinctOrderingFilter(
        choices=(("-created", _("Most recent")),),
        empty_label=None,
        widget=OrderingWidget,
    )

    search = FreeTextFilter(
        widget=FreeTextFilterWidget,
        fields=["name", "description"],
    )

    organisation = django_filters.ModelChoiceFilter(
        queryset=apps.get_model(settings.A4_ORGANISATIONS_MODEL).objects.order_by(
            "name"
        ),
        widget=OrganisationWidget,
    )

    is_archived = django_filters.BooleanFilter(widget=ArchivedWidget)

    created = django_filters.NumberFilter(
        field_name="created",
        lookup_expr="year",
        widget=YearWidget,
    )

    administrative_district = django_filters.ModelChoiceFilter(
        queryset=AdministrativeDistrict.objects.all(), widget=DistrictWidget
    )

    class Meta:
        model = project_models.Project
        fields = [
            "search",
            "organisation",
            "is_archived",
            "created",
            "administrative_district",
        ]


class ParticipantInviteDetailView(generic.DetailView):
    model = models.ParticipantInvite
    slug_field = "token"
    slug_url_kwarg = "invite_token"

    def dispatch(self, request, invite_token, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                "project-participant-invite-update", invite_token=invite_token
            )
        else:
            return super().dispatch(request, *args, **kwargs)


class ParticipantInviteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.ParticipantInvite
    form_class = forms.ParticipantInviteForm
    slug_field = "token"
    slug_url_kwarg = "invite_token"

    def form_valid(self, form):
        if form.is_accepted():
            form.instance.accept(self.request.user)
            return redirect(form.instance.project.get_absolute_url())
        else:
            form.instance.reject()
            return redirect("/")


class ModeratorInviteDetailView(generic.DetailView):
    model = models.ModeratorInvite
    slug_field = "token"
    slug_url_kwarg = "invite_token"

    def dispatch(self, request, invite_token, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                "project-moderator-invite-update", invite_token=invite_token
            )
        else:
            return super().dispatch(request, *args, **kwargs)


class ModeratorInviteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.ModeratorInvite
    form_class = forms.ModeratorInviteForm
    slug_field = "token"
    slug_url_kwarg = "invite_token"

    def form_valid(self, form):
        if form.is_accepted():
            form.instance.accept(self.request.user)
            return redirect(form.instance.project.get_absolute_url())
        else:
            form.instance.reject()
            return redirect("/")


class AbstractProjectUserInviteListView(
    ProjectMixin,
    a4dashboard_mixins.DashboardBaseMixin,
    a4dashboard_mixins.DashboardComponentMixin,
    generic.base.TemplateResponseMixin,
    generic.edit.FormMixin,
    generic.detail.SingleObjectMixin,
    generic.edit.ProcessFormView,
):
    form_class = forms.InviteUsersFromEmailForm
    invite_model = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "submit_action" in request.POST:
            if request.POST["submit_action"] == "remove_user":
                pk = int(request.POST["user_pk"])
                user = get_object_or_404(User, pk=pk)
                related_users = getattr(self.object, self.related_users_field)
                related_users.remove(user)
                messages.success(request, self.success_message_removal)
            elif request.POST["submit_action"] == "remove_invite":
                pk = int(request.POST["invite_pk"])
                if self.invite_model.objects.filter(pk=pk).exists():
                    invite = self.invite_model.objects.get(pk=pk)
                    invite.delete()
                    messages.success(request, _("Invitation succesfully removed."))
                else:
                    messages.info(
                        request, _("Invitation was already accepted or removed.")
                    )

            response = redirect(self.get_success_url())
        else:
            response = super().post(request, *args, **kwargs)

        self._send_component_updated_signal()
        return response

    def filter_existing(self, emails):
        related_users = getattr(self.object, self.related_users_field)
        related_emails = [u.email for u in related_users.all()]
        existing = []
        filtered_emails = []
        for email in emails:
            if email in related_emails:
                existing.append(email)
            else:
                filtered_emails.append(email)
        return filtered_emails, existing

    def filter_pending(self, emails):
        pending = []
        filtered_emails = []
        for email in emails:
            if self.invite_model.objects.filter(
                email=email, project=self.project
            ).exists():
                pending.append(email)
            else:
                filtered_emails.append(email)
        return filtered_emails, pending

    def form_valid(self, form):
        emails = list(
            set(
                itertools.chain(
                    form.cleaned_data["add_users"],
                    form.cleaned_data["add_users_upload"],
                )
            )
        )

        emails, existing = self.filter_existing(emails)
        if existing:
            messages.error(
                self.request,
                _("Following users already accepted an invitation: ")
                + ", ".join(existing),
            )

        emails, pending = self.filter_pending(emails)
        if pending:
            messages.error(
                self.request,
                _("Following users are already invited: ") + ", ".join(pending),
            )

        for email in emails:
            self.invite_model.objects.invite(self.request.user, self.project, email)

        messages.success(
            self.request,
            ngettext(
                self.success_message[0], self.success_message[1], len(emails)
            ).format(len(emails)),
        )

        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["labels"] = (self.add_user_field_label, self.add_user_upload_field_label)
        return kwargs

    def _send_component_updated_signal(self):
        a4dashboard_signals.project_component_updated.send(
            sender=self.component.__class__,
            project=self.project,
            component=self.component,
            user=self.request.user,
        )


class DashboardProjectModeratorsView(AbstractProjectUserInviteListView):
    model = project_models.Project
    slug_url_kwarg = "project_slug"
    template_name = "meinberlin_projects/project_moderators.html"
    permission_required = "a4projects.change_project"
    menu_item = "project"

    related_users_field = "moderators"
    add_user_field_label = _("Invite moderators via email")
    add_user_upload_field_label = _("Invite moderators via file upload")
    success_message = (_("{} moderator invited."), _("{} moderators invited."))
    success_message_removal = _("Moderator successfully removed.")

    invite_model = models.ModeratorInvite

    def get_permission_object(self):
        return self.project


class DashboardProjectParticipantsView(AbstractProjectUserInviteListView):
    model = project_models.Project
    slug_url_kwarg = "project_slug"
    template_name = "meinberlin_projects/project_participants.html"
    permission_required = "a4projects.change_project"
    menu_item = "project"

    related_users_field = "participants"
    add_user_field_label = _("Invite users via email")
    add_user_upload_field_label = _("Invite users via file upload")
    success_message = (_("{} participant invited."), _("{} participants invited."))
    success_message_removal = _("Participant successfully removed.")

    invite_model = models.ParticipantInvite

    def get_permission_object(self):
        return self.project


class ProjectDetailView(PermissionRequiredMixin, BplanProjectDispatchMixin):
    model = models.Project
    permission_required = "a4projects.view_project"

    def get_permission_object(self):
        return self.project

    def get_template_names(self):
        if self.project.project_type == "meinberlin_bplan.Bplan":
            return ["meinberlin_projects/project_bplan_detail.html"]
        return ["meinberlin_projects/project_detail.html"]

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = self.project.offlineevent_set.all().order_by("date")
        context["edit_link"] = reverse(
            "a4dashboard:project-edit", kwargs={"project_slug": self.project.slug}
        )
        return models.ProjectInsight.update_context(self.project, context)


class ProjectEventView(PermissionRequiredMixin, generic.DetailView):
    model = OfflineEvent
    permission_required = "meinberlin_offlineevents.view_offlineevent"
    slug_url_kwarg = "event_slug"
    template_name = "meinberlin_projects/project_event.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.object.project
        context["edit_link"] = reverse(
            "a4dashboard:offlineevent-update", kwargs={"slug": self.object.slug}
        )
        return context


class ModuleDetailview(PermissionRequiredMixin, PhaseDispatchMixin):
    model = module_models.Module
    permission_required = "a4projects.view_project"
    slug_url_kwarg = "module_slug"

    @cached_property
    def project(self):
        return self.module.project

    @cached_property
    def module(self):
        return self.get_object()

    def get_permission_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        """Append project and module to the template context."""
        if "project" not in kwargs:
            kwargs["project"] = self.project
        if "module" not in kwargs:
            kwargs["module"] = self.module
        return super().get_context_data(**kwargs)


class ProjectInformationView(PermissionRequiredMixin, generic.DetailView):
    model = models.Project
    template_name = "meinberlin_projects/project_information.html"
    permission_required = "a4projects.view_project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_link"] = reverse(
            "a4dashboard:dashboard-information-edit",
            kwargs={"project_slug": self.object.slug},
        )
        return context


class ProjectResultsView(PermissionRequiredMixin, generic.DetailView):
    model = models.Project
    template_name = "meinberlin_projects/project_results.html"
    permission_required = "a4projects.view_project"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_link"] = reverse(
            "a4dashboard:dashboard-result-edit",
            kwargs={"project_slug": self.object.slug},
        )
        return context
