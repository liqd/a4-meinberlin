from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from meinberlin.apps.cms.viewsets import project_chooser_viewset

ProjectSelectionBlock = project_chooser_viewset.get_block_class(
    name="ProjectSelectionBlock", module_path="meinberlin.apps.cms.blocks"
)


class ProjectsWrapperBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=80)
    projects = blocks.ListBlock(ProjectSelectionBlock(label="Project"), min_num=3)

    class Meta:
        template = "meinberlin_cms/blocks/projects_block.html"
        icon = "list-ul"


class ButtonBlock(blocks.StructBlock):
    link_text = blocks.CharBlock(required=True)
    link = blocks.URLBlock(
        required=True,
        help_text=_("Please enter a full url which starts with https://"),
        max_length=500,
    )
    style = blocks.ChoiceBlock(
        choices=[("light", "light"), ("fulltone", "fulltone"), ("primary", "primary")],
        default="primary",
    )

    class Meta:
        template = "meinberlin_cms/blocks/button_block.html"


class UserActionBarBlock(blocks.StructBlock):
    body_logged_in = blocks.RichTextBlock(
        label="Body",
        help_text=_("Use '%username%' in the text to display the username"),
    )
    buttons_logged_in = blocks.ListBlock(ButtonBlock(), label="Buttons")
    body_anonymous = blocks.RichTextBlock(label="Body")
    buttons_anonymous = blocks.ListBlock(ButtonBlock(), label="Buttons")

    class Meta:
        template = "meinberlin_cms/blocks/user_action_bar_block.html"
        form_template = "meinberlin_cms/blocks/user_action_bar_block_form.html"
        icon = "user"

    def get_form_context(self, value, prefix="", errors=None):
        context = super().get_form_context(value, prefix, errors)
        context["logged_in_fields"] = [
            context["children"]["body_logged_in"],
            context["children"]["buttons_logged_in"],
        ]
        context["anonymous_fields"] = [
            context["children"]["body_anonymous"],
            context["children"]["buttons_anonymous"],
        ]
        return context

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        request = context["request"]

        if request.user.is_authenticated:
            context["body"] = str(value["body_logged_in"]).replace(
                "%username%", request.user.username
            )
            context["buttons"] = value["buttons_logged_in"]
        else:
            context["body"] = value["body_anonymous"]
            context["buttons"] = value["buttons_anonymous"]
        return context


class IconBlock(blocks.StructBlock):
    image = ImageBlock()
    body = blocks.RichTextBlock()

    class Meta:
        template = "meinberlin_cms/blocks/icon_block.html"
        icon = "image"


class IconListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=False,
        help_text=_("Optional title for the list of panels."),
    )
    icon_list_blocks = blocks.ListBlock(IconBlock())

    class Meta:
        template = "meinberlin_cms/blocks/icon_list_block.html"
        icon = "list-ul"
        label = _("Icon List")


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


class TeaserBlock(blocks.StructBlock):
    alignment = blocks.ChoiceBlock(
        choices=[
            ("left", _("Left")),
            ("right", _("Right")),
        ],
        default="left",
        help_text=_("Should the image be on the left or on the right?"),
    )
    title = blocks.CharBlock(max_length=70)
    body = blocks.RichTextBlock(max_length=250)
    button = ButtonBlock(required=False, form_classname="w-field w-panel")
    image = ImageBlock(form_classname="w-field w-panel")

    class Meta:
        template = "meinberlin_cms/blocks/teaser_block.html"
        icon = "view"


class LinkBlock(blocks.StructBlock):
    link_text = blocks.CharBlock(required=True)
    link = blocks.PageChooserBlock(
        required=True,
    )

    class Meta:
        icon = "link"


class InfoBarBlock(blocks.StructBlock):
    body = blocks.RichTextBlock()
    image = ImageBlock(required=False, form_classname="w-field w-panel")
    link = LinkBlock(required=False, form_classname="w-field w-panel")

    class Meta:
        template = "meinberlin_cms/blocks/info_bar_block.html"
        icon = "info-circle"


class ExternalLinkBlock(blocks.StructBlock):
    link_text = blocks.CharBlock(required=True)
    link = blocks.URLBlock(
        required=True,
        help_text=_("Please enter a full url which starts with https://"),
        max_length=500,
    )

    class Meta:
        icon = "link-external"
