from wagtail.wagtailcore.blocks import CharBlock, PageChooserBlock, StructBlock


class LinkBlock(StructBlock):
    link = PageChooserBlock(required=True)
link_text = CharBlock(required=True)
