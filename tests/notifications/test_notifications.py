from datetime import timedelta

import pytest
from dateutil.parser import parse
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from freezegun import freeze_time

from adhocracy4.actions.verbs import Verbs
from adhocracy4.phases.models import Phase
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.notifications.models import Notification
from meinberlin.config import settings

START = Verbs.START.value

EVENT_STARTING_HOURS = 0
if hasattr(settings, "ACTIONS_OFFLINE_EVENT_STARTING_HOURS"):
    EVENT_STARTING_HOURS = settings.ACTIONS_OFFLINE_EVENT_STARTING_HOURS
else:
    EVENT_STARTING_HOURS = 72


@pytest.mark.django_db
def test_event_soon_notification(offline_event_factory):
    EVENT_DATE = parse("2020-01-05 17:00:00 UTC")

    event = offline_event_factory(
        date=EVENT_DATE,
    )

    notification_count = Notification.objects.filter(
        action__obj_content_type__model="OfflineEvent",
    ).count()
    assert notification_count == 0

    with freeze_time(event.date - timedelta(hours=5)):
        call_command("create_offlineevent_system_actions")
        notification = Notification.objects.filter(
            action__obj_content_type__model="offlineevent",
        )
        assert len(notification) == 1


@pytest.mark.django_db
def test_phase_started_email(apiclient, phase_factory, proposal_factory):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    phase.end_date += timedelta(hours=48)
    phase.save()
    phase.refresh_from_db()

    content_type = ContentType.objects.get_for_model(Phase)
    notification_count = Notification.objects.filter(
        action__verb=START, action__obj_content_type=content_type
    ).count()
    assert notification_count == 0

    with freeze_phase(phase):
        call_command("create_system_actions")
        notification_count = Notification.objects.filter(
            action__verb=START, action__obj_content_type=content_type
        ).count()
        assert notification_count == 1
