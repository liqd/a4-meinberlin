from django.utils.translation import gettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import views


# Even though the OfflineEventPhase is never used show need one PhaseContent in order for the Module to work properly
class OfflineEventPhase(phases.PhaseContent):
    """Phase for a offline event."""

    app = apps.Config.label
    phase = "offline-event"
    view = views.OfflineEventModuleDetailView

    name = _("Offline Event")
    description = _("Manage a single offline event")
    module_name = _("Offline Event")

    # No features needed - OfflineEventItem is managed through module dashboard
    features = {}


phases.content.register(OfflineEventPhase())
