import pytest
from django.core import mail
from django.urls import reverse


@pytest.mark.django_db
def test_heading_levels_are_normalised(platform_email_factory):
    assert platform_email_factory(body="<h1>Title</h1>").body == "<h2>Title</h2>"
    assert platform_email_factory(body="<h5>Title</h5>").body == "<p>Title</p>"


@pytest.mark.django_db
def test_body_for_email_has_inline_styles(platform_email_factory):
    platform_email = platform_email_factory(body="<h2>Heading</h2>")

    assert '<h2 style="font-size:22px;' in platform_email.body_for_email


@pytest.mark.django_db
def test_sent_email_contains_styled_heading(
    client, user_factory, email_address_factory
):
    admin = user_factory(is_superuser=True)
    email_address_factory(user=admin, email=admin.email, primary=True, verified=True)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "<h2>Heading</h2><p>Body text</p>",
        "send": "Send",
    }

    url = reverse("meinberlin_platformemails:create")
    client.login(username=admin.email, password="password")
    client.post(url, data)

    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    html = message.alternatives[0][0]

    assert '<h2 style="font-size:22px;' in html
    assert "<h2" not in message.body
    assert "Heading" in message.body
