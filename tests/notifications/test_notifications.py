from datetime import timedelta

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command

from adhocracy4.actions.verbs import Verbs
from adhocracy4.phases.models import Phase
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.notifications.models import Notification

START = Verbs.START.value


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
