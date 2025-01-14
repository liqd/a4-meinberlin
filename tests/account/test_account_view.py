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
