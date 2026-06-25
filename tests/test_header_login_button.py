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
