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


class MenuItem(models.Model):
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='+',
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=255, verbose_name="Title")

    subpages = StreamField(
        [('link', LinkBlock())],
        blank=True,
        null=True,
        help_text='These Links will be displayed in as a dropdown menu',
        verbose_name='Submenu'
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
        FieldPanel('menu_name', classname='full title'),
        InlinePanel('menu_items', label="Menu Items")
    ]


class HeaderMenuItem(Orderable, MenuItem):
parent = ParentalKey('cms_snippets.HeaderMenu', related_name='menu_items')
