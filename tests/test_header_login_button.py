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
    assert "js-auth-modal-body" in html
    assert "js-auth-modal-close" in html


@pytest.mark.django_db
def test_header_login_triggers_open_modal(client):
    response = client.get("/")
    html = response.content.decode()

    # Login icon in the service area and login/register links in the burger menu
    assert 'class="service-button-overlay__form js-auth-modal-open"' in html
    assert html.count('class="hamburger-nav__link js-auth-modal-open"') == 2
    assert html.count("js-auth-modal-open") == 3


@pytest.mark.django_db
def test_header_auth_modal_not_rendered_for_authenticated_user(client, user):
    client.force_login(user)
    response = client.get("/")
    html = response.content.decode()
    assert 'id="auth-modal"' not in html
    assert "js-auth-modal-open" not in html
