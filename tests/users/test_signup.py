import pytest
from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from meinberlin.apps.users.models import User


@pytest.mark.django_db
def test_signup_user_notifications_checked(client):
    resp = client.post(
        reverse("account_signup"),
        {
            "username": "dauser",
            "email": "mail@example.com",
            "get_newsletters": "on",
            "get_notifications": "on",
            "password1": "password",
            "password2": "password",
            "terms_of_use": "on",
            "captcha": "testpass:0",
        },
    )
    assert resp.status_code == 302
    user = User.objects.get()
    assert user.notification_settings.email_newsletter
    assert user.notification_settings.notify_creator


@pytest.mark.django_db
def test_signup_user_newsletter_checked(client):
    resp = client.post(
        reverse("account_signup"),
        {
            "username": "dauser",
            "email": "mail@example.com",
            "get_newsletters": "on",
            "password1": "password",
            "password2": "password",
            "terms_of_use": "on",
            "captcha": "testpass:0",
        },
    )
    assert resp.status_code == 302
    user = User.objects.get()
    assert user.notification_settings.email_newsletter
    assert not user.notification_settings.notify_creator


@pytest.mark.django_db
def test_signup_user_newsletter_not_checked(client):
    resp = client.post(
        reverse("account_signup"),
        {
            "username": "dauser",
            "email": "mail@example.com",
            "password1": "password",
            "password2": "password",
            "terms_of_use": "on",
            "captcha": "testpass:0",
        },
    )
    assert resp.status_code == 302
    user = User.objects.get()
    assert not user.notification_settings.email_newsletter


@pytest.mark.django_db
def test_signup_user_unchecked_terms_of_use(client):
    resp = client.post(
        reverse("account_signup"),
        {
            "username": "dauser",
            "email": "mail@example.com",
            "password1": "password",
            "password2": "password",
            "captcha": "testpass:0",
        },
    )
    assert User.objects.count() == 0
    assert not resp.context["form"].is_valid()
    assert list(resp.context["form"].errors.keys()) == ["terms_of_use"]


@override_settings()
@pytest.mark.django_db
def test_signup_user_without_captcha(client):
    del settings.CAPTCHA_URL
    resp = client.post(
        reverse("account_signup"),
        {
            "username": "dauser",
            "email": "mail@example.com",
            "get_newsletters": "on",
            "password1": "password",
            "password2": "password",
            "terms_of_use": "on",
        },
    )
    assert resp.status_code == 302
    user = User.objects.get()
    assert user.notification_settings.email_newsletter


@override_settings()
@pytest.mark.django_db
def test_signup_user_with_captcha_url_as_empty_string(client):
    settings.CAPTCHA_URL = ""
    resp = client.post(
        reverse("account_signup"),
        {
            "username": "dauser",
            "email": "mail@example.com",
            "get_newsletters": "on",
            "password1": "password",
            "password2": "password",
            "terms_of_use": "on",
        },
    )
    assert resp.status_code == 302
    user = User.objects.get()
    assert user.notification_settings.email_newsletter
