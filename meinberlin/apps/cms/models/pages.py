from django.db import models
from wagtail import blocks
from wagtail import fields
from wagtail.admin import panels
from wagtail.models import Page

from meinberlin.apps.actions import blocks as actions_blocks
from meinberlin.apps.cms import blocks as cms_blocks


class SimplePage(Page):
    body = fields.RichTextField(blank=True)

    content_panels = [
        panels.TitleFieldPanel("title"),
        panels.FieldPanel("body"),
    ]

    subpage_types = []


class StreamfieldSimplePage(Page):
    body = fields.StreamField(
        [("paragraph", blocks.RichTextBlock()), ("html", blocks.RawHTMLBlock())],
        blank=True,
    )

    content_panels = [
        panels.TitleFieldPanel("title"),
        panels.FieldPanel("body"),
    ]

    subpage_types = []


class HomePage(Page):
    body = fields.StreamField(
        [
            (
                "paragraph",
                blocks.RichTextBlock(
                    template="meinberlin_cms/blocks/richtext_block.html"
                ),
            ),
            ("projects", cms_blocks.ProjectsWrapperBlock()),
            ("user_action_bar", cms_blocks.UserActionBarBlock()),
            ("image_call_to_action", cms_blocks.ImageCallToActionBlock()),
            ("columns_text", cms_blocks.ColumnsBlock()),
            ("activities", actions_blocks.PlatformActivityBlock()),
            ("accordion_list", cms_blocks.AccordionListBlock()),
            ("teaser", cms_blocks.TeaserBlock()),
            ("map_teaser", cms_blocks.MapTeaserBlock()),
        ],
    )
    subtitle = models.CharField(max_length=120)

    header_image = models.ForeignKey(
        "meinberlin_cms.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        panels.FieldPanel("subtitle"),
        panels.FieldPanel("header_image"),
        panels.FieldPanel("body"),
    ]


class DocsPage(Page):
    body = fields.StreamField(
        [
            ("accordion_list", cms_blocks.AccordionListBlock()),
            ("header", blocks.CharBlock(template="meinberlin_cms/blocks/header.html")),
        ],
    )

    description = fields.RichTextField(blank=True)

    content_panels = Page.content_panels + [
        panels.FieldPanel("description"),
        panels.FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Documents"

    subpage_types = []
