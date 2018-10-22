from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                PageChooserPanel)
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailadmin import edit_handlers
from wagtail.wagtailsnippets.models import register_snippet

from cms.snippets.blocks import LinkBlock


class HeaderItem(models.Model):
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='+',
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=255, verbose_name="Title")

    header_image = models.ForeignKey(
        'meinberlin_cms.CustomImage',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def url(self):
        return self.link_page.url

    def __str__(self):
        return self.title

    panels = [
        PageChooserPanel('link_page'),
        FieldPanel('title'),
        edit_handlers.StreamFieldPanel('subpages')
    ]


@register_snippet
class HeaderMenu(ClusterableModel):
    menu_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.menu_name

    panels = [
        edit_handlers.FieldPanel('title'),
        edit_handlers.InlinePanel('items')
    ]


class HeaderMenuItem(Orderable, MenuItem):
    parent = ParentalKey('meinberlin_cms.HeaderMenu', related_name='items')
