from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components
from adhocracy4.dashboard.components.forms import ModuleFormComponent
from adhocracy4.dashboard.dashboard import ModulePhasesComponent, ModuleBasicComponent

from . import forms as offline_forms
from . import views

# Registry für offline Modulklassen registrieren (Blueprint-Typ "OE")
from meinberlin.apps.dashboard import register_offline_module_blueprint_type
register_offline_module_blueprint_type("OE")


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

class OfflineEventModuleComponent(DashboardComponent):
    identifier = "module_offlineevent"    
    label = _("Offline Event")
    weight = 1

    def is_effective(self, module):
        return module.blueprint_type == "OE"

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse(
            "a4dashboard:offlineevent-module",
            kwargs={
                "module_slug": module.slug,
            },
        )

    def get_urls(self):
        return [
            (
                r"^modules/(?P<module_slug>[-\w_]+)/offlineevent-module/$",
                views.OfflineEventModuleDashboardView.as_view(component=self),
                "offlineevent-module",
            )
        ]

components.register_module(OfflineEventModuleComponent())


class OfflineEventSettingsComponent(DashboardComponent):
    identifier = "offlineevent_settings"
    weight = 12
    label = _("Date And Time")

    def is_effective(self, module):
        return module.blueprint_type == "OE"

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse(
            "a4dashboard:offlineevent-settings",
            kwargs={
                "module_slug": module.slug,
            },
        )

    def get_urls(self):
        return [
            (
                r"^modules/(?P<module_slug>[-\w_]+)/offlineevent-settings/$",
                views.OfflineEventSettingsDashboardView.as_view(component=self),
                "offlineevent-settings",
            )
        ]

components.register_module(OfflineEventSettingsComponent())

# Hides the Phase Component for Offline Event Modules
class OfflineEventPhasesComponent(ModulePhasesComponent):
    identifier = "phases"
    def is_effective(self, module):
        return module.blueprint_type != "OE"

components.replace_module(OfflineEventPhasesComponent())

# Hides the Basic Component for Offline Event Modules
class OfflineEventBasicComponent(ModuleBasicComponent):
    identifier = "module_basic"
    def is_effective(self, module):
        return module.blueprint_type != "OE"

components.replace_module(OfflineEventBasicComponent())
