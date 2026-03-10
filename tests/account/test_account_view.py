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


@pytest.mark.django_db
def test_show_restricted_moderator_in_notifications_view(client, project):
    notifications_url = reverse(
        "notifications",
    )
    anonymous, moderator, initiator = setup_users(project)
    client.login(username=moderator.email, password="password")
    resp = client.get(notifications_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_show_restricted_initiator_in_notifications_view(client, project):
    notifications_url = reverse(
        "notifications",
    )
    anonymous, moderator, initiator = setup_users(project)
    client.login(username=initiator.email, password="password")
    resp = client.get(notifications_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_default_data_in_notifications_view(client, user):
    notifications_url = reverse(
        "notifications",
    )
    client.login(username=user.email, password="password")
    resp = client.get(notifications_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_altered_data_in_notifications_view(client, user):
    notifications_url = reverse(
        "notifications",
    )
    client.login(username=user.email, password="password")
    user.notification_settings.update_all_settings(False, email_newsletter=True)
    resp = client.get(notifications_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_notifications_page_contains_links_to_saved_searches_and_followed_projects(
    client, user
):
    notifications_url = reverse("notifications")
    search_profiles_url = reverse("search_profiles")
    followed_projects_url = reverse("followed_projects")

    client.login(username=user.email, password="password")
    resp = client.get(notifications_url)

    assert resp.status_code == 200
    assert search_profiles_url in resp.content.decode()
    assert followed_projects_url in resp.content.decode()
