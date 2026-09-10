from datetime import timedelta

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.management import call_command

from adhocracy4.actions.verbs import Verbs
from adhocracy4.phases.models import Phase
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.notifications.models import Notification
from meinberlin.test.helpers import GuestUserCreator

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


@pytest.mark.django_db
def test_guest_comment_notifies_proposal_creator(
    phase_factory, proposal_factory, comment_factory
):
    """
    A comment by a guest creates an in-app notification for the proposal
    creator and sends them the notification email. Guests receive no mail.
    """
    guest = GuestUserCreator().create_guest_user()
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase
    )
    creator = proposal.creator
    # clear the default moderators so only the creator email is expected
    project.moderators.clear()

    mail.outbox.clear()
    comment_factory(content_object=proposal, creator=guest)

    notifications = Notification.objects.filter(recipient=creator)
    assert notifications.count() == 1
    assert notifications.first().action.type == "comment"
    assert notifications.first().action.actor == guest

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [creator.email]
    assert not any(guest.email in message.to for message in mail.outbox)
