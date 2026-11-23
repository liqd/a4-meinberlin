import pytest
from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from meinberlin.apps.users.models import User


@pytest.mark.django_db
def test_signup_renders_password_criteria(client):
    resp = client.get(reverse("account_signup"))
    assert resp.status_code == 200
    content = resp.content.decode()
    assert "data-password-criteria" in content
    assert 'id="id_password1_criteria"' in content
    assert 'data-password-input="#id_password1"' in content
    assert 'data-criterion="length"' in content
    assert 'data-criterion="username"' in content
    assert 'data-criterion="categories"' in content


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


@override_settings(
    A4_CAPTCHA_TYPE="cap",
    A4_CAP_CAPTCHA_ENDPOINT="https://cap.example.com/sitekey/",
    A4_CAP_CAPTCHA_SECRET="secret",
    A4_CAP_CAPTCHA_WIDGET_URL="https://cdn.jsdelivr.net/npm/cap-widget@0.1.63",
)
def test_signup_form_uses_cap_widget():
    from adhocracy4.captcha.widgets import CapCaptchaWidget
    from meinberlin.apps.users.forms import TermsSignupForm

    form = TermsSignupForm()

    assert "captcha" in form.fields
    assert isinstance(form.fields["captcha"].widget, CapCaptchaWidget)


@override_settings(
    A4_CAPTCHA_TYPE="cap",
    A4_CAP_CAPTCHA_ENDPOINT="",
    A4_CAP_CAPTCHA_SECRET="",
    A4_CAP_CAPTCHA_WIDGET_URL="",
)
def test_signup_form_removes_captcha_when_cap_is_not_configured():
    from meinberlin.apps.users.forms import TermsSignupForm

    form = TermsSignupForm()

    assert "captcha" not in form.fields


@override_settings(
    A4_CAPTCHA_TYPE="cap",
    A4_CAP_CAPTCHA_ENDPOINT="https://cap.example.com/sitekey/",
    A4_CAP_CAPTCHA_SECRET="secret",
    A4_CAP_CAPTCHA_WIDGET_URL="https://cdn.jsdelivr.net/npm/cap-widget@0.1.63",
)
@pytest.mark.django_db
def test_signup_with_cap_captcha(client):
    resp = client.post(
        reverse("account_signup"),
        {
            "username": "capuser",
            "email": "cap@example.com",
            "password1": "password",
            "password2": "password",
            "terms_of_use": "on",
            "captcha": "testpass",
        },
    )

    assert resp.status_code == 302
    assert User.objects.filter(username="capuser").exists()
