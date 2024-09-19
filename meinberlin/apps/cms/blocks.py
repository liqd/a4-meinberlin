from django import forms
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from adhocracy4.projects.models import Access
from adhocracy4.projects.models import Project


class ProjectSelectionBlock(blocks.ChooserBlock):
    target_model = Project
    widget = forms.widgets.Select

    @cached_property
    def field(self):
        return forms.ModelChoiceField(
            queryset=self.target_model.objects.filter(
                Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
                is_draft=False,
                is_archived=False,
            ),
            widget=self.widget,
            required=self._required,
            help_text=self._help_text,
        )

    def value_for_form(self, value):
        if isinstance(value, Project):
            return value.pk
        return value

    def value_from_form(self, value):
        # if project became unavailable (unpublished), selection will become an
        # empty string and cause a server error on save, so we give a fallback
        value = value or None
        return super().value_from_form(value)


class ProjectsWrapperBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=80)
    projects = blocks.ListBlock(
        ProjectSelectionBlock(label="Project"),
    )

    class Meta:
        template = "meinberlin_cms/blocks/projects_block.html"
        icon = "list-ul"


class CallToActionBlock(blocks.StructBlock):
    body = blocks.RichTextBlock()
    link = blocks.CharBlock()
    link_text = blocks.CharBlock(max_length=50, label="Link Text")

    class Meta:
        template = "meinberlin_cms/blocks/cta_block.html"
        icon = "plus-inverse"


class ImageCallToActionBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(max_length=80)
    body = blocks.RichTextBlock()
    link = blocks.CharBlock()
    link_text = blocks.CharBlock(max_length=50, label="Link Text")

    class Meta:
        template = "meinberlin_cms/blocks/image_cta_block.html"
        icon = "image"


class ColumnsBlock(blocks.StructBlock):
    columns_count = blocks.ChoiceBlock(
        choices=[
            (2, "Two columns"),
            (3, "Three columns"),
            (4, "Four columns"),
        ],
        default=2,
    )

    columns = blocks.ListBlock(
        blocks.RichTextBlock(label="Column body"),
    )

    class Meta:
        template = "meinberlin_cms/blocks/columns_block.html"
        icon = "grip"


class AccordionBlock(blocks.StructBlock):
    expand_accordion = blocks.BooleanBlock(
        required=False,
        help_text=_(
            "The accordion is collapsed by default. Select this option to have it expanded when the page loads."
        ),
        label=_("Expand accordion?"),
    )
    title = blocks.CharBlock()
    body = blocks.RichTextBlock(required=False)

    class Meta:
        template = "meinberlin_cms/blocks/accordion_block.html"
        icon = "arrow-down"


class AccordionListBlock(blocks.StructBlock):
    list_title = blocks.CharBlock(
        required=False, help_text=_("Optional title for the list of accordions.")
    )
    accordions = blocks.ListBlock(
        AccordionBlock(), help_text=_("Add, remove, or reorder accordions.")
    )

    class Meta:
        template = "meinberlin_cms/blocks/accordion_list_block.html"
        icon = "list-ul"
        label = _("Accordion List")


class InfographicBlock(blocks.StructBlock):
    text_left = blocks.CharBlock(max_length=50)
    text_center = blocks.CharBlock(max_length=50)
    text_right = blocks.CharBlock(max_length=50)

    class Meta:
        template = "meinberlin_cms/blocks/infographic_block.html"
        icon = "success"


class MapTeaserBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    body = blocks.RichTextBlock()

    class Meta:
        template = "meinberlin_cms/blocks/map_teaser_block.html"
        icon = "view"


class LinkBlock(blocks.StructBlock):
    link_text = blocks.CharBlock(required=True)
    link = blocks.PageChooserBlock(
        required=True,
    )

    class Meta:
        icon = "link"


class ExternalLinkBlock(blocks.StructBlock):
    link_text = blocks.CharBlock(required=True)
    link = blocks.URLBlock(
        required=True,
        help_text=_("Please enter a full url which starts with https:// " "or http://"),
        max_length=500,
    )

    class Meta:
        icon = "link-external"
