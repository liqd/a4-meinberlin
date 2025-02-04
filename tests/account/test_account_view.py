import json

import pytest
from django.urls import reverse

from adhocracy4.test.helpers import setup_users


@pytest.mark.django_db
def test_show_restricted_false_in_notifications_view(client, user):
    notifications_url = reverse(
        "notifications",
    )
    client.login(username=user.email, password="password")
    resp = client.get(notifications_url)
    assert resp.status_code == 200
    assert not resp.context["show_restricted"]


@pytest.mark.django_db
def test_show_restricted_moderator_in_notifications_view(client, project):
    notifications_url = reverse(
        "notifications",
    )
    anonymous, moderator, initiator = setup_users(project)
    client.login(username=moderator.email, password="password")
    resp = client.get(notifications_url)
    assert resp.status_code == 200
    assert resp.context["show_restricted"]


@pytest.mark.django_db
def test_show_restricted_initiator_in_notifications_view(client, project):
    notifications_url = reverse(
        "notifications",
    )
    anonymous, moderator, initiator = setup_users(project)
    client.login(username=initiator.email, password="password")
    resp = client.get(notifications_url)
    assert resp.status_code == 200
    assert resp.context["show_restricted"]


@pytest.mark.django_db
def test_default_data_in_notifications_view(client, user):
    notifications_url = reverse(
        "notifications",
    )
    client.login(username=user.email, password="password")
    resp = client.get(notifications_url)
    assert resp.status_code == 200
    data = json.loads(resp.context["data"])
    assert data["email_newsletter"] is False
    assert data["notify_followers_phase_started"] is True
    assert data["notify_followers_phase_over_soon"] is True
    assert data["notify_followers_event_upcoming"] is True
    assert data["notify_creator"] is True
    assert data["notify_creator_on_moderator_feedback"] is True
    assert data["notify_initiators_project_created"] is True
    assert data["notify_moderator"] is True


@pytest.mark.django_db
def test_altered_data_in_notifications_view(client, user):
    notifications_url = reverse(
        "notifications",
    )
    client.login(username=user.email, password="password")
    user.notification_settings.update_all_settings(False, email_newsletter=True)
    resp = client.get(notifications_url)
    assert resp.status_code == 200
    data = json.loads(resp.context["data"])
    assert data["email_newsletter"] is True
    assert data["notify_followers_phase_started"] is False
    assert data["notify_followers_phase_over_soon"] is False
    assert data["notify_followers_event_upcoming"] is False
    assert data["notify_creator"] is False
    assert data["notify_creator_on_moderator_feedback"] is False
    assert data["notify_initiators_project_created"] is False
    assert data["notify_moderator"] is False
