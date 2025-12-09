from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components
from adhocracy4.dashboard.dashboard import ModuleBasicComponent
from adhocracy4.dashboard.dashboard import ModulePhasesComponent
from meinberlin.apps.dashboard import register_event_module

from . import models as offline_models
from . import views

# Offline Event Module Component Area


class OfflineEventModuleComponent(DashboardComponent):
    identifier = "module_offlineevent"
    label = _("Offline Event")
    weight = 1

    def is_effective(self, module):
        return module.blueprint_type == "OE"

    def get_progress(self, module):
        required_fields = ["name", "event_type", "description"]
        item = offline_models.OfflineEventItem.objects.filter(module=module).first()
        if not item:
            return 0, len(required_fields)
        num_valid = 0
        for field in required_fields:
            value = getattr(item, field, None)
            if value:
                num_valid += 1
        return num_valid, len(required_fields)

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
        item = offline_models.OfflineEventItem.objects.filter(module=module).first()
        if not item:
            return 0, 1
        return (1, 1) if getattr(item, "event_date", None) else (0, 1)

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

ModulePhasesComponent.hide_for("OE")
ModuleBasicComponent.hide_for("OE")
register_event_module("OE")
