import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas import phases
from meinberlin.apps.ideas.models import Idea


@pytest.mark.django_db
def test_can_delete_own_idea(apiclient, idea_factory, phase_factory):
    collect_phase, module, project, idea = setup_phase(
        phase_factory,
        idea_factory,
        phases.CollectPhase,
    )
    apiclient.force_authenticate(user=idea.creator)
    url = reverse("items-detail", args=[idea.id])

    with freeze_phase(collect_phase):
        assert Idea.objects.count() == 1
        response = apiclient.delete(url, format="json")
        assert response.status_code == 204
        assert Idea.objects.count() == 0
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1


@pytest.mark.django_db
def test_cant_delete_other_idea(apiclient, user, idea_factory, phase_factory):
    collect_phase, module, project, idea = setup_phase(
        phase_factory,
        idea_factory,
        phases.CollectPhase,
    )
    apiclient.force_authenticate(user=user)
    url = reverse("items-detail", args=[idea.id])

    with freeze_phase(collect_phase):
        assert Idea.objects.count() == 1
        response = apiclient.delete(url, format="json")
        assert response.status_code == 403
        assert Idea.objects.count() == 1


@pytest.mark.django_db
def test_superuser_can_delete_idea(apiclient, user_factory, user, idea_factory):
    admin = user_factory(is_superuser=True)
    idea = idea_factory(creator=user)
    apiclient.force_authenticate(user=admin)
    url = reverse("items-detail", args=[idea.id])

    assert Idea.objects.count() == 1
    response = apiclient.delete(url, format="json")
    print(response.data)
    assert response.status_code == 204
    assert Idea.objects.count() == 0


@pytest.mark.django_db
def test_moderator_can_delete_idea(apiclient, user, idea_factory):
    idea = idea_factory(creator=user)
    moderator = idea.module.project.moderators.first()
    apiclient.force_authenticate(user=moderator)
    url = reverse("items-detail", args=[idea.id])

    assert Idea.objects.count() == 1
    response = apiclient.delete(url, format="json")
    assert response.status_code == 204
    assert Idea.objects.count() == 0
