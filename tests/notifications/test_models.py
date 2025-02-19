from datetime import timedelta

import factory
import pytest
from django.conf import settings
from django.core.management import call_command
from django.db.models.signals import post_save
from freezegun import freeze_time

from adhocracy4.actions.models import Action
from adhocracy4.actions.signals import _add_action
from adhocracy4.follows.models import Follow
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.notifications.models import Notification

EVENT_STARTING_HOURS = 0
if hasattr(settings, "ACTIONS_OFFLINE_EVENT_STARTING_HOURS"):
    EVENT_STARTING_HOURS = settings.ACTIONS_OFFLINE_EVENT_STARTING_HOURS
else:
    EVENT_STARTING_HOURS = 72


@factory.django.mute_signals(post_save)
@pytest.mark.django_db
def test_should_notify_on_comment(idea_factory, comment_factory):
    idea = idea_factory()
    comment = comment_factory(content_object=idea)
    _add_action(None, comment, True, None)
    action = Action.objects.last()

    should_notify, recipients = Notification.should_notify(action)
    assert len(recipients) == 1
    assert recipients[0] == idea.creator
    assert should_notify


@factory.django.mute_signals(post_save)
@pytest.mark.django_db
def test_should_notify_on_like(idea_factory, rating_factory):
    idea = idea_factory()
    rating = rating_factory(content_object=idea)
    _add_action(None, rating, True, None)
    action = Action.objects.last()

    should_notify, recipients = Notification.should_notify(action)
    assert len(recipients) == 1
    assert recipients[0] == idea.creator
    assert should_notify


@factory.django.mute_signals(post_save)
@pytest.mark.django_db
def test_should_notify_on_remark(moderator_remark_factory):
    remark = moderator_remark_factory()
    _add_action(None, remark, True, None)
    action = Action.objects.last()

    should_notify, recipients = Notification.should_notify(action)
    assert len(recipients) == 1
    assert recipients[0] == remark.item.creator
    assert should_notify


@factory.django.mute_signals(post_save)
@pytest.mark.django_db
def test_should_notify_on_phase_start(
    user_factory, follow_factory, phase_factory, proposal_factory
):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase, module__project__follow=[]
    )
    phase.end_date += timedelta(hours=48)
    phase.save()
    phase.refresh_from_db()
    user1 = user_factory()
    user2 = user_factory()
    user3 = user_factory()
    Follow.objects.all().delete()
    follow_factory(creator=user1, project=project)
    follow_factory(creator=user2, project=project)
    follow_factory(creator=user3, project=project, enabled=False)

    with freeze_phase(phase):
        call_command("create_system_actions")
        action = Action.objects.last()
        should_notify, recipients = Notification.should_notify(action)
        recipients = recipients.order_by("pk")
        assert len(recipients) == 2
        assert list(recipients) == [user1, user2]
        assert should_notify


@factory.django.mute_signals(post_save)
@pytest.mark.django_db
def test_should_notify_on_event_start(
    user_factory, follow_factory, offline_event_factory
):
    event = offline_event_factory()
    user1 = user_factory()
    user2 = user_factory()
    user3 = user_factory()
    Follow.objects.all().delete()
    follow_factory(creator=user1, project=event.project)
    follow_factory(creator=user2, project=event.project)
    follow_factory(creator=user3, project=event.project, enabled=False)

    with freeze_time(event.date - timedelta(hours=5)):
        call_command("create_offlineevent_system_actions")
        action = Action.objects.last()
        should_notify, recipients = Notification.should_notify(action)
        recipients = recipients.order_by("pk")
        assert len(recipients) == 2
        assert list(recipients) == [user1, user2]
        assert should_notify
