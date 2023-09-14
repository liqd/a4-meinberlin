from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin import panels
from wagtail.fields import StreamField
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet

from meinberlin.apps.cms import blocks as cms_blocks


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    link_page = models.ForeignKey("wagtailcore.Page", on_delete=models.CASCADE)

    @property
    def url(self):
        return self.link_page.url

    def __str__(self):
        return self.title

    panels = [panels.FieldPanel("title"), panels.PageChooserPanel("link_page")]


@register_snippet
class NavigationMenu(ClusterableModel):
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title

    panels = [panels.FieldPanel("title"), panels.InlinePanel("items")]


class NavigationMenuItem(Orderable, MenuItem):
    parent = ParentalKey("meinberlin_cms.NavigationMenu", related_name="items")


class FooterMenuItem(models.Model):
    section_title = models.CharField(max_length=255)
    link_page = StreamField([("link", cms_blocks.LinkBlock())], use_json_field=True)

    @property
    def url(self):
        return self.link_page.url

    def __str__(self):
        return self.section_title

    panels = [panels.FieldPanel("section_title"), panels.PageChooserPanel("link_page")]


@register_snippet
class FooterNavigationMenu(ClusterableModel):
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title

    panels = [panels.FieldPanel("title"), panels.InlinePanel("items")]


class FooterNavigationMenuItem(Orderable, MenuItem):
    parent = ParentalKey("meinberlin_cms.FooterNavigationMenu", related_name="items")
