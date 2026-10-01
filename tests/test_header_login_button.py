import pytest


@pytest.mark.django_db
def test_header_login_logout_button(client, user):
    response = client.get("/")
    html = response.content.decode()
    assert "servicebuttonAccount" in html
    assert "fa-user" in html
    assert html.index("servicebuttonAccount") < html.index("servicebuttonMenu")

    client.force_login(user)
    response = client.get("/")
    html = response.content.decode()
    assert "fa-user-check" in html


@pytest.mark.django_db
def test_header_auth_modal_markup(client):
    response = client.get("/")
    html = response.content.decode()
    assert 'id="auth-modal"' in html
    assert 'id="auth-modal-body"' in html
    assert "js-auth-modal-close" in html
    assert 'hx-boost="true"' in html


@pytest.mark.django_db
def test_header_login_triggers_open_modal(client):
    response = client.get("/")
    html = response.content.decode()

    assert 'id="auth-modal-body"' in html
    # Header login icon + burger login/register links point at the modal body
    assert 'hx-get="/accounts/login/"' in html
    assert 'hx-get="/accounts/signup/' in html
    assert 'hx-target="#auth-modal-body"' in html


@pytest.mark.django_db
def test_header_auth_modal_not_rendered_for_authenticated_user(client, user):
    client.force_login(user)
    response = client.get("/")
    html = response.content.decode()
    assert 'id="auth-modal"' not in html
    assert 'hx-target="#auth-modal-body"' not in html
