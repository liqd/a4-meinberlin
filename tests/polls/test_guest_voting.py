from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from adhocracy4.polls.phases import VotingPhase
from adhocracy4.projects.enums import Access
from adhocracy4.test.factories import polls as poll_factories
from meinberlin.test.helpers import GuestUserCreator


def create_poll(phase_factory, allow_guest_users, allow_unregistered_users=False):
    poll = poll_factories.PollFactory()
    project = poll.module.project
    project.access = Access.PUBLIC
    project.is_draft = False
    project.allow_guest_users = allow_guest_users
    project.save()
    poll.allow_unregistered_users = allow_unregistered_users
    poll.save()

    question = poll_factories.QuestionFactory(poll=poll)
    poll_factories.ChoiceFactory(question=question)
    poll_factories.ChoiceFactory(question=question)

    now = timezone.now()
    phase_factory(
        module=poll.module,
        phase_content=VotingPhase(),
        start_date=now - timedelta(days=1),
        end_date=now + timedelta(days=1),
    )
    return poll, question


@pytest.mark.django_db
def test_poll_can_vote_for_guest_when_project_allows_guests(apiclient, phase_factory):
    poll, _ = create_poll(phase_factory, allow_guest_users=True)
    guest = GuestUserCreator().create_guest_user()
    apiclient.force_authenticate(user=guest)

    response = apiclient.get(reverse("polls-detail", kwargs={"pk": poll.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["can_vote"] is True


@pytest.mark.django_db
def test_poll_can_not_vote_for_guest_when_project_disallows_guests(
    apiclient, phase_factory
):
    poll, _ = create_poll(phase_factory, allow_guest_users=False)
    guest = GuestUserCreator().create_guest_user()
    apiclient.force_authenticate(user=guest)

    response = apiclient.get(reverse("polls-detail", kwargs={"pk": poll.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["can_vote"] is False


@pytest.mark.django_db
def test_poll_can_vote_for_anonymous_when_poll_allows_unregistered(
    apiclient, phase_factory
):
    poll, _ = create_poll(
        phase_factory,
        allow_guest_users=False,
        allow_unregistered_users=True,
    )

    response = apiclient.get(reverse("polls-detail", kwargs={"pk": poll.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["can_vote"] is True


@pytest.mark.django_db
def test_poll_can_not_vote_for_anonymous_without_unregistered_voting(
    apiclient, phase_factory
):
    poll, _ = create_poll(
        phase_factory,
        allow_guest_users=False,
        allow_unregistered_users=False,
    )

    response = apiclient.get(reverse("polls-detail", kwargs={"pk": poll.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["can_vote"] is False
