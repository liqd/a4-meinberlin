from django.utils.translation import gettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class OfflineEventPhase(phases.PhaseContent):
    """Phase for a single offline event."""

    app = apps.Config.label
    phase = "offline-event"
    view = views.OfflineEventDetailView

    name = _("Offline Event")
    description = _("Maqnage a single offline event")
    module_name = _("Offline Event")

    features = {
        "crud": (models.OfflineEvent,),
    }


phases.content.register(OfflineEventPhase())
