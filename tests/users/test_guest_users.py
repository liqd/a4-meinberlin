from datetime import timedelta

import pytest
from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.core import mail
from django.core.management import call_command
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone
from guest_user.functions import get_guest_model
from guest_user.functions import is_guest_user
from rest_framework.test import APIRequestFactory

from adhocracy4.projects.enums import Access
from meinberlin.apps.notifications.models import Notification
from meinberlin.apps.users.emails import WelcomeEmail
from meinberlin.apps.users.models import User
from meinberlin.apps.users.permissions import IsRegularUser
from meinberlin.apps.users.predicates import is_regular_user
from meinberlin.test.helpers import GuestUserCreator

# -- shared primitives --------------------------------------------------------


@pytest.mark.django_db
def test_is_regular_user_predicate(user):
    guest = GuestUserCreator().create_guest_user()

    assert is_regular_user(user)
    assert not is_regular_user(guest)
    assert not is_regular_user(AnonymousUser())


@pytest.mark.django_db
def test_is_regular_user_permission(user):
    guest = GuestUserCreator().create_guest_user()
    permission = IsRegularUser()
    factory = APIRequestFactory()

    request = factory.get("/")
    request.user = user
    assert permission.has_permission(request, None)

    request.user = guest
    assert not permission.has_permission(request, None)

    request.user = AnonymousUser()
    assert not permission.has_permission(request, None)


# -- guest creation -----------------------------------------------------------


@pytest.mark.django_db
def test_guest_create_view_creates_guest(client):
    assert User.objects.count() == 0

    response = client.post(
        reverse("guest_create"),
        {"terms_of_use": "on", "captcha": "testpass:0"},
    )

    assert response.status_code == 302
    assert User.objects.count() == 1
    assert is_guest_user(User.objects.get())


@pytest.mark.django_db
def test_guest_create_view_requires_terms(client):
    response = client.post(
        reverse("guest_create"),
        {"captcha": "testpass:0"},
    )

    assert User.objects.count() == 0
    assert not response.context["form"].is_valid()


@pytest.mark.django_db
def test_guest_create_view_redirects_authenticated(client, user):
    client.force_login(user)
    response = client.get(reverse("guest_create"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_guest_cannot_be_authenticated_by_identifier_alone():
    """No auth backend may accept a guest without the (unknown) password."""
    guest = GuestUserCreator().create_guest_user()
    request = RequestFactory().get("/")

    assert authenticate(request, username=guest.email, password="wrong") is None
    assert authenticate(request, username=guest.username, password="wrong") is None


@pytest.mark.django_db
def test_guest_cannot_relogin_via_login_form(client):
    """A guest's public name must not be usable to log back in."""
    guest = GuestUserCreator().create_guest_user()

    for login_value in (guest.email, guest.username):
        response = client.post(
            reverse("account_login"),
            {"login": login_value, "password": "wrong", "remember": ""},
        )
        assert not response.wsgi_request.user.is_authenticated


# -- participation rule -------------------------------------------------------


@pytest.mark.django_db
def test_guest_may_participate_when_allowed(project_factory):
    project = project_factory(
        access=Access.PUBLIC, is_draft=False, allow_guest_users=True
    )
    guest = GuestUserCreator().create_guest_user()
    assert guest.has_perm("a4projects.participate_in_project", project)


@pytest.mark.django_db
def test_guest_may_not_participate_when_disallowed(project_factory):
    project = project_factory(
        access=Access.PUBLIC, is_draft=False, allow_guest_users=False
    )
    guest = GuestUserCreator().create_guest_user()
    assert not guest.has_perm("a4projects.participate_in_project", project)


@pytest.mark.django_db
def test_regular_user_participates_regardless_of_guest_flag(project_factory, user):
    project = project_factory(
        access=Access.PUBLIC, is_draft=False, allow_guest_users=False
    )
    assert user.has_perm("a4projects.participate_in_project", project)


# -- API gating ---------------------------------------------------------------


@pytest.mark.django_db
def test_follows_api_blocked_for_guest(apiclient):
    guest = GuestUserCreator().create_guest_user()
    apiclient.force_authenticate(user=guest)
    response = apiclient.get(reverse("follows-list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_follows_api_allowed_for_regular_user(apiclient, user):
    apiclient.force_authenticate(user=user)
    response = apiclient.get(reverse("follows-list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_notifications_api_blocked_for_guest(apiclient):
    guest = GuestUserCreator().create_guest_user()
    apiclient.force_authenticate(user=guest)
    response = apiclient.get(reverse("notifications-list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_notifications_api_allowed_for_regular_user(apiclient, user):
    apiclient.force_authenticate(user=user)
    response = apiclient.get(reverse("notifications-list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_guest_cannot_reach_notification_settings(client):
    guest = GuestUserCreator().create_guest_user()
    client.force_login(guest)

    response = client.get(reverse("notification_settings"))

    assert response.status_code == 302
    assert response.url != reverse("notification_settings")


@pytest.mark.django_db
def test_kiezradar_api_blocked_for_guest(apiclient):
    guest = GuestUserCreator().create_guest_user()
    apiclient.force_authenticate(user=guest)
    response = apiclient.get(reverse("kiezradar-list"))
    assert response.status_code == 403


# -- outbound email exclusion -------------------------------------------------


def test_exclude_guest_users_keeps_strings():
    from meinberlin.apps.contrib.emails import Email

    # plain email strings (e.g. external notifications) are always kept
    assert Email._exclude_guest_users(["a@example.com"]) == ["a@example.com"]


@pytest.mark.django_db
def test_welcome_email_skips_guest_users():
    guest = GuestUserCreator().create_guest_user()
    mail.outbox = []
    WelcomeEmail.send(guest)
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_welcome_email_sent_to_regular_user(user):
    mail.outbox = []
    WelcomeEmail.send(user)
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_guest_gets_in_app_notification_but_no_email(comment_factory, user_factory):
    """Guests keep in-app notification rows for post-convert backlog; no outbound mail."""
    from meinberlin.test.factories.ideas import IdeaFactory

    guest = GuestUserCreator().create_guest_user()
    idea = IdeaFactory(creator=guest)
    commenter = user_factory()

    mail.outbox.clear()
    comment_factory(content_object=idea, creator=commenter)

    assert Notification.objects.filter(recipient=guest).count() == 1
    assert not any(guest.email in message.to for message in mail.outbox)


# -- conversion ---------------------------------------------------------------


@pytest.mark.django_db
def test_email_confirmed_deletes_guest_row():
    guest = GuestUserCreator().create_guest_user()
    GuestModel = get_guest_model()
    assert GuestModel.objects.filter(user=guest).exists()

    email_address = EmailAddress.objects.create(
        user=guest, email="converted@example.com", verified=True, primary=True
    )
    email_confirmed.send(
        sender=EmailAddress,
        request=RequestFactory().get("/"),
        email_address=email_address,
    )

    assert not GuestModel.objects.filter(user=guest).exists()


@pytest.mark.django_db
def test_guest_convert_view_converts_account(client):
    guest = GuestUserCreator().create_guest_user()
    client.force_login(guest)

    response = client.post(
        reverse("guest_convert"),
        {
            "username": "converteduser",
            "email": "converted@example.com",
            "password1": "a-good-password",
            "password2": "a-good-password",
            "terms_of_use": "on",
            "get_notifications": "on",
        },
    )

    assert response.status_code == 302
    guest.refresh_from_db()
    assert guest.username == "converteduser"
    assert guest.email == "converted@example.com"
    assert guest.check_password("a-good-password")


# -- contribution-aware cleanup ----------------------------------------------


def _make_guest_expired(guest, days=20):
    """Backdate the Guest row past the cleanup cutoff (created_at is auto-set)."""
    GuestModel = get_guest_model()
    GuestModel.objects.filter(user=guest).update(
        created_at=timezone.now() - timedelta(days=days)
    )


@pytest.mark.django_db
def test_cleanup_deletes_old_empty_guest():
    guest = GuestUserCreator().create_guest_user()
    _make_guest_expired(guest)

    call_command("delete_expired_guests")

    assert not User.objects.filter(pk=guest.pk).exists()


@pytest.mark.django_db
def test_cleanup_keeps_recent_empty_guest():
    guest = GuestUserCreator().create_guest_user()

    call_command("delete_expired_guests")

    assert User.objects.filter(pk=guest.pk).exists()


@pytest.mark.django_db
def test_cleanup_keeps_old_guest_with_contribution():
    from meinberlin.test.factories.ideas import IdeaFactory

    guest = GuestUserCreator().create_guest_user()
    _make_guest_expired(guest)
    IdeaFactory(creator=guest)

    call_command("delete_expired_guests")

    assert User.objects.filter(pk=guest.pk).exists()


@pytest.mark.django_db
def test_cleanup_dry_run_deletes_nothing():
    guest = GuestUserCreator().create_guest_user()
    _make_guest_expired(guest)

    call_command("delete_expired_guests", "--dry-run")

    assert User.objects.filter(pk=guest.pk).exists()
