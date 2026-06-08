import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_redirect_from_referer(client, user, login_url):
    target_url = reverse("notification_settings")
    login_page = client.get(
        login_url,
        HTTP_REFERER=f"http://testserver{target_url}",
    )
    assert login_page.context["redirect_field_value"] == target_url

    response = client.post(
        login_url,
        {
            "login": user.email,
            "password": "password",
            "next": login_page.context["redirect_field_value"],
        },
    )
    assert response.status_code == 302
    assert response.url == target_url
