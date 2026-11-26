import pytest
from django.core import mail
from django.urls import reverse

from adhocracy4.follows import models as follow_models
from meinberlin.apps.newsletters import models


@pytest.mark.django_db
def test_heading_tags_are_kept(newsletter_factory):
    newsletter = newsletter_factory(body="<h2>Heading</h2><p>Text</p>")

    assert "<h2>Heading</h2>" in newsletter.body
    assert "<p>Text</p>" in newsletter.body


@pytest.mark.django_db
@pytest.mark.parametrize(
    "raw,expected",
    [
        ("<h1>Title</h1>", "<h2>Title</h2>"),
        ("<h2>Title</h2>", "<h2>Title</h2>"),
        ("<h3>Title</h3>", "<h3>Title</h3>"),
        ("<h4>Title</h4>", "<h4>Title</h4>"),
        ("<h5>Title</h5>", "<p>Title</p>"),
        ("<h6>Title</h6>", "<p>Title</p>"),
    ],
)
def test_heading_levels_are_normalised(newsletter_factory, raw, expected):
    newsletter = newsletter_factory(body=raw)

    assert newsletter.body == expected


@pytest.mark.django_db
def test_heading_attributes_are_stripped(newsletter_factory):
    newsletter = newsletter_factory(
        body='<h2 class="title" style="font-size:80px" id="anchor">Title</h2>'
    )

    assert newsletter.body == "<h2>Title</h2>"


@pytest.mark.django_db
def test_aria_heading_is_converted(newsletter_factory):
    newsletter = newsletter_factory(
        body='<div role="heading" aria-level="2">Title</div>'
    )

    assert newsletter.body == "<h2>Title</h2>"


@pytest.mark.django_db
def test_body_for_email_has_inline_styles(newsletter_factory):
    newsletter = newsletter_factory(body="<h2>Heading</h2>")

    body = newsletter.body_for_email

    assert body.startswith("<h2 style=")
    assert "font-size:22px" in body
    assert "line-height:28px" in body
    assert "font-weight:bold" in body
    assert "margin-top:28px" in body


@pytest.mark.django_db
def test_body_for_email_without_headings_is_unchanged(newsletter_factory):
    body = "<p>Some <strong>text</strong></p><ul><li>Item</li></ul>"
    newsletter = newsletter_factory(body=body)

    assert newsletter.body_for_email == newsletter.body_with_absolute_urls


@pytest.mark.django_db
def test_body_text_strips_markup(newsletter_factory):
    newsletter = newsletter_factory(
        body="<h2>Heading</h2><p>Some text</p><ul><li>Item</li></ul>"
    )

    text = newsletter.body_text

    assert "Heading" in text
    assert "Some text" in text
    assert "- Item" in text
    assert "<" not in text


@pytest.mark.django_db
def test_body_text_keeps_link_targets(newsletter_factory):
    newsletter = newsletter_factory(
        body='<p><a href="https://example.com">Example</a></p>'
    )

    assert "Example (https://example.com)" in newsletter.body_text


@pytest.mark.django_db
def test_cache_is_invalidated(newsletter_factory):
    newsletter = newsletter_factory(body="<h2>First</h2>")
    assert "First" in newsletter.body_for_email

    newsletter.body = "<h2>Second</h2>"

    assert "Second" in newsletter.body_for_email
    assert "First" not in newsletter.body_for_email
    assert "First" not in newsletter.body_text


@pytest.mark.django_db
def test_sent_email_contains_styled_heading(
    admin, client, project, user_factory, follow_factory, email_address_factory
):
    organisation = project.organisation
    user = user_factory(get_newsletters=True)
    email_address_factory(user=user, email=user.email, primary=True, verified=True)
    follow_models.Follow.objects.all().delete()
    follow_factory(creator=user, project=project)

    data = {
        "sender_name": "Tester",
        "sender": "test@test.de",
        "subject": "Testsubject",
        "body": "<h2>Heading</h2><p>Body text</p>",
        "receivers": models.ORGANISATION,
        "organisation": organisation.pk,
        "project": "",
        "send": "Send",
    }

    url = reverse(
        "a4dashboard:newsletter-create", kwargs={"organisation_slug": organisation.slug}
    )
    client.login(username=admin.email, password="password")
    client.post(url, data)

    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    html = message.alternatives[0][0]

    assert '<h2 style="font-size:22px;' in html
    assert "<h2" not in message.body
    assert "Heading" in message.body
