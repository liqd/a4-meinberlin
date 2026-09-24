import pytest
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response

HTMX = {"HX-Request": "true"}


@pytest.mark.django_db
def test_login_htmx_renders_fragment(client, login_url):
    response = client.get(login_url, headers=HTMX)
    assert response.status_code == 200
    assert_template_response(response, "account/login_content.html")
    assert b"<html" not in response.content


@pytest.mark.django_db
def test_login_htmx_success_sets_redirect_header(client, user, login_url):
    response = client.post(
        login_url,
        {"login": user.email, "password": "password"},
        headers=HTMX,
    )
    assert response.status_code == 204
    assert response.headers["HX-Redirect"]


@pytest.mark.django_db
def test_login_htmx_invalid_renders_fragment(client, user, login_url):
    response = client.post(
        login_url,
        {"login": user.email, "password": "wrong_password"},
        headers=HTMX,
    )
    assert response.status_code == 200
    assert_template_response(response, "account/login_content.html")


@pytest.mark.django_db
def test_signup_htmx_renders_fragment(client, signup_url):
    response = client.get(signup_url, headers=HTMX)
    assert response.status_code == 200
    assert_template_response(response, "account/signup_content.html")
    assert b"<html" not in response.content


@pytest.mark.django_db
def test_guest_htmx_renders_fragment(client):
    url = reverse("guest_create")
    response = client.get(url, headers=HTMX)
    assert response.status_code == 200
    assert_template_response(response, "meinberlin_users/guest_create_content.html")
    assert b"<html" not in response.content
