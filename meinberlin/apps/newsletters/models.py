import re

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4 import transforms
from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects.models import Project
from meinberlin.apps.contrib import email_transforms

PLATFORM = 0
ORGANISATION = 1
PROJECT = 2
INITIATOR = 3

RECEIVER_CHOICES = (
    (PROJECT, _("Users following a specific project")),
    (ORGANISATION, _("Users following a project of your organisation")),
    (INITIATOR, _("Every initiator of your organisation")),
    (PLATFORM, _("Every user of the platform")),
)


class Newsletter(UserGeneratedContentModel):
    sender_name = models.CharField(max_length=254, verbose_name=_("Name"))
    sender = models.EmailField(blank=True, verbose_name=_("Sender"))
    subject = models.CharField(max_length=254, verbose_name=_("Subject"))
    body = CKEditor5Field(
        blank=True,
        config_name="email-editor",
        verbose_name=_("Email body"),
        validators=[ImageAltTextValidator()],
    )
    sent = models.DateTimeField(blank=True, null=True, verbose_name=_("Sent"))

    receivers = models.PositiveSmallIntegerField(
        choices=RECEIVER_CHOICES, verbose_name=_("Receivers")
    )

    project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.CASCADE
    )

    organisation = models.ForeignKey(
        settings.A4_ORGANISATIONS_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )

    @cached_property
    def body_with_absolute_urls(self):
        return self.replace_relative_media_urls(self.body)

    @cached_property
    def body_for_email(self):
        """Body as sent in the HTML part: absolute URLs and inline styles."""
        return email_transforms.render_for_email(self.body_with_absolute_urls)

    @cached_property
    def body_text(self):
        """Body as sent in the plain text part: no markup, URLs kept."""
        return email_transforms.html_to_text(self.body_with_absolute_urls)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        # Delete cached properties
        if key == "body":
            for name in ("body_with_absolute_urls", "body_for_email", "body_text"):
                try:
                    delattr(self, name)
                except AttributeError:
                    pass

    @staticmethod
    def replace_relative_media_urls(text):
        if not settings.MEDIA_URL.startswith("/"):
            # Replace only if MEDIA_URL is relative
            return text

        # Find every occurrence of the MEDIA_URL that is either following a
        # whitespace, an equal sign or a quotation mark.
        pattern = re.compile(r'([\s="\'])(%s)' % re.escape(settings.MEDIA_URL))
        text = re.sub(pattern, r"\1%s\2" % settings.WAGTAILADMIN_BASE_URL, text)
        return text

    def save(self, update_fields=None, *args, **kwargs):
        self.body = transforms.clean_html_field(
            email_transforms.normalise_body(self.body), "email-editor"
        )
        if update_fields:
            update_fields = {"body"}.union(update_fields)
        super().save(update_fields=update_fields, *args, **kwargs)
