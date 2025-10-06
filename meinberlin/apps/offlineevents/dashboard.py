from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components
from adhocracy4.dashboard.components.forms import ModuleFormComponent

from . import forms as offline_forms
from . import views


class OfflineEventsComponent(DashboardComponent):
    identifier = "offlineevents"
    weight = 20
    label = _("Offline Events")

    def is_effective(self, project):
        return True

    def get_progress(self, project):
        return 0, 0

    def get_base_url(self, project):
        return reverse(
            "a4dashboard:offlineevent-list", kwargs={"project_slug": project.slug}
        )

    def get_urls(self):
        return [
            (
                r"^offlineevents/projects/(?P<project_slug>[-\w_]+)/$",
                views.OfflineEventListView.as_view(component=self),
                "offlineevent-list",
            ),
            (
                r"^offlineevents/create/project/(?P<project_slug>[-\w_]+)/$",
                views.OfflineEventCreateView.as_view(component=self),
                "offlineevent-create",
            ),
            (
                r"^offlineevents/(?P<slug>[-\w_]+)/update/$",
                views.OfflineEventUpdateView.as_view(component=self),
                "offlineevent-update",
            ),
            (
                r"^offlineevents/(?P<slug>[-\w_]+)/delete/$",
                views.OfflineEventDeleteView.as_view(component=self),
                "offlineevent-delete",
            ),
        ]


components.register_project(OfflineEventsComponent())


class OfflineEventSettingsComponent(ModuleFormComponent):
    identifier = "offlineevent_settings"
    weight = 12
    label = _("Date And Time")
    form_title = _("Edit Date and Time")
    form_class = offline_forms.OfflineEventSettingsForm
    form_template_name = "a4dashboard/includes/module_offlineevent_settings_form.html"


components.register_module(OfflineEventSettingsComponent())
