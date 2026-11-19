from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from adhocracy4.follows.models import Follow
from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from meinberlin.apps.ideas import models as idea_models
from meinberlin.apps.ideas import phases
from meinberlin.apps.projects import follow_suggestions
from meinberlin.test.helpers import GuestUserCreator


def claim_url(project):
    return reverse("follow_suggestion_claim", kwargs={"slug": project.slug})


@pytest.mark.django_db
def test_claim_shows_once_within_thirty_days(client, project_factory, user):
    project = project_factory(access=Access.PUBLIC, is_draft=False)
    client.force_login(user)

    response = client.post(claim_url(project))

    assert response.json() == {"show": True}
    user.refresh_from_db()
    assert user.follow_suggestion_shown_at is not None

    response = client.post(claim_url(project))

    assert response.json() == {"show": False}


@pytest.mark.django_db
def test_claim_shows_again_after_thirty_days(client, project_factory, user):
    project = project_factory(access=Access.PUBLIC, is_draft=False)
    client.force_login(user)
    user.follow_suggestion_shown_at = timezone.now() - timedelta(days=31)
    user.save(update_fields=["follow_suggestion_shown_at"])

    response = client.post(claim_url(project))

    assert response.json() == {"show": True}


@pytest.mark.django_db
def test_claim_not_shown_when_already_following(client, project_factory, user):
    project = project_factory(access=Access.PUBLIC, is_draft=False)
    Follow.objects.create(project=project, creator=user)
    client.force_login(user)

    response = client.post(claim_url(project))

    assert response.json() == {"show": False}
    user.refresh_from_db()
    assert user.follow_suggestion_shown_at is None


@pytest.mark.django_db
def test_claim_stores_timestamp_on_guest_account(client, project_factory):
    project = project_factory(access=Access.PUBLIC, is_draft=False)
    guest = GuestUserCreator().create_guest_user()
    client.force_login(guest)

    response = client.post(claim_url(project))

    assert response.json() == {"show": True}
    guest.refresh_from_db()
    assert guest.follow_suggestion_shown_at is not None


@pytest.mark.django_db
def test_claim_uses_session_for_anonymous_visitors(client, project_factory):
    project = project_factory(access=Access.PUBLIC, is_draft=False)

    response = client.post(claim_url(project))

    assert response.json() == {"show": True}
    assert follow_suggestions.FOLLOW_SUGGESTION_SHOWN_SESSION_KEY in client.session

    response = client.post(claim_url(project))

    assert response.json() == {"show": False}


@pytest.mark.django_db
def test_anonymous_session_limit_expires_after_thirty_days(client, project_factory):
    project = project_factory(access=Access.PUBLIC, is_draft=False)
    client.post(claim_url(project))

    session = client.session
    session[follow_suggestions.FOLLOW_SUGGESTION_SHOWN_SESSION_KEY] = (
        timezone.now() - timedelta(days=31)
    ).timestamp()
    session.save()

    response = client.post(claim_url(project))

    assert response.json() == {"show": True}


@pytest.mark.django_db
def test_follow_marker_follows_project_and_shows_confirmation(
    client, project_factory, user
):
    project = project_factory(access=Access.PUBLIC, is_draft=False)
    client.force_login(user)
    url = reverse("project-detail", kwargs={"slug": project.slug})

    response = client.get(url, {"follow": project.slug})

    assert response.status_code == 302
    assert response.url == url
    assert Follow.objects.filter(project=project, creator=user, enabled=True).exists()

    response = client.get(response.url)

    content = response.content.decode()
    assert "data-follow-suggestion" in content
    assert 'data-follow-suggestion-state="confirmation-auth"' in content
    assert 'class="alert__headline"' in content
    assert reverse("notification_settings") in content
    assert reverse("followed_projects") in content


@pytest.mark.django_db
def test_follow_marker_is_ignored_for_guest_accounts(client, project_factory):
    project = project_factory(access=Access.PUBLIC, is_draft=False)
    guest = GuestUserCreator().create_guest_user()
    client.force_login(guest)
    url = reverse("project-detail", kwargs={"slug": project.slug})

    response = client.get(url, {"follow": project.slug})

    assert response.status_code == 200
    assert not Follow.objects.filter(project=project, creator=guest).exists()


@pytest.mark.django_db
def test_banner_not_rendered_when_already_following(client, project_factory, user):
    project = project_factory(access=Access.PUBLIC, is_draft=False)
    Follow.objects.create(project=project, creator=user)
    client.force_login(user)

    response = client.get(reverse("project-detail", kwargs={"slug": project.slug}))

    assert "data-follow-suggestion" not in response.content.decode()


@pytest.mark.django_db
def test_trigger_is_suppressed_within_thirty_days(client, project_factory, user):
    project = project_factory(access=Access.PUBLIC, is_draft=False)
    client.force_login(user)
    user.follow_suggestion_shown_at = timezone.now() - timedelta(days=10)
    user.save(update_fields=["follow_suggestion_shown_at"])

    session = client.session
    session[follow_suggestions.FOLLOW_SUGGESTION_TRIGGER_SESSION_KEY] = project.pk
    session.save()

    response = client.get(reverse("project-detail", kwargs={"slug": project.slug}))

    assert "data-follow-suggestion" not in response.content.decode()


@pytest.mark.django_db
def test_idea_creation_triggers_banner(client, phase_factory, category_factory, user):
    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})
    client.login(username=user.email, password="password")

    with freeze_phase(phase):
        response = client.post(
            url,
            {
                "name": "Idea",
                "description": "description",
                "category": category.pk,
            },
        )

        assert response.status_code == 302
        assert idea_models.Idea.objects.count() == 1

        response = client.get(response["Location"])

    content = response.content.decode()
    assert "data-follow-suggestion" in content
    assert 'data-initial-trigger="true"' in content


@pytest.mark.django_db
def test_guest_convert_preserves_next_url(client):
    guest = GuestUserCreator().create_guest_user()
    client.force_login(guest)
    next_url = "/projekte/project/?follow=project"

    response = client.get(reverse("guest_convert"), {"next": next_url})

    assert response.status_code == 200
    assert response.context["next"] == next_url
    assert 'name="next"' in response.content.decode()
