from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import MultiFieldPanel
from wagtail.admin.panels import ObjectList
from wagtail.admin.panels import PageChooserPanel
from wagtail.admin.panels import TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.models import register_setting


@register_setting
class HeaderPages(BaseSiteSetting):
    help_page = models.ForeignKey(
        "wagtailcore.Page",
        related_name="help_page",
        verbose_name="Help Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Please add a link to the help page."),
    )
    feedback_page = models.ForeignKey(
        "wagtailcore.Page",
        related_name="feedback_page",
        verbose_name="Feedback Form Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Please add a link to the feedback form page."),
    )
    # accessibility settings
    feedback_name = models.CharField(max_length=255, blank=True)
    feedback_email = models.EmailField(max_length=255, blank=True)
    feedback_phone = models.CharField(max_length=255, blank=True)
    additional_external_info = models.URLField(
        help_text=_("Add link for additional information"), blank=True
    )
    additional_external_info_link_text = models.CharField(max_length=255, blank=True)
    accessibility_declaration = models.ForeignKey(
        "wagtailcore.Page",
        related_name="accessibility_declaration_page",
        verbose_name="Accessibility Decleration Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Please add a link to your accesibility decleration page."),
    )
    accessibility_declaration_link_text = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("help_page"),
        FieldPanel("feedback_page"),
        MultiFieldPanel(
            [
                FieldPanel("feedback_name"),
                FieldPanel("feedback_email"),
                FieldPanel("feedback_phone"),
            ],
            heading=_("Accessibility Feedback Contact Information"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("accessibility_declaration"),
                FieldPanel("accessibility_declaration_link_text"),
            ],
            heading="Accessibility Declaration",
        ),
        MultiFieldPanel(
            [
                FieldPanel("additional_external_info"),
                FieldPanel("additional_external_info_link_text"),
            ],
            heading=_("Additional Information on Accessibility"),
        ),
    ]
