# Generated by Django 4.2.11 on 2024-09-03 15:09

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_cms", "0044_add_a11y_header_pages_and_footer_menu"),
    ]

    operations = [
        migrations.AlterField(
            model_name="docspage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "documents_list",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "expand_accordion",
                                    wagtail.blocks.BooleanBlock(
                                        help_text="The accordion is collapsed by default. Select this option to have it expanded when the page loads.",
                                        label="Expand accordion?",
                                        required=False,
                                    ),
                                ),
                                ("title", wagtail.blocks.CharBlock()),
                                ("body", wagtail.blocks.RichTextBlock(required=False)),
                            ]
                        ),
                    ),
                    (
                        "header",
                        wagtail.blocks.CharBlock(
                            template="meinberlin_cms/blocks/header.html"
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "paragraph",
                        wagtail.blocks.RichTextBlock(
                            template="meinberlin_cms/blocks/richtext_block.html"
                        ),
                    ),
                    (
                        "call_to_action",
                        wagtail.blocks.StructBlock(
                            [
                                ("body", wagtail.blocks.RichTextBlock()),
                                ("link", wagtail.blocks.CharBlock()),
                                (
                                    "link_text",
                                    wagtail.blocks.CharBlock(
                                        label="Link Text", max_length=50
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "image_call_to_action",
                        wagtail.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("title", wagtail.blocks.CharBlock(max_length=80)),
                                ("body", wagtail.blocks.RichTextBlock()),
                                ("link", wagtail.blocks.CharBlock()),
                                (
                                    "link_text",
                                    wagtail.blocks.CharBlock(
                                        label="Link Text", max_length=50
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "columns_text",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "columns_count",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            (2, "Two columns"),
                                            (3, "Three columns"),
                                            (4, "Four columns"),
                                        ]
                                    ),
                                ),
                                (
                                    "columns",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.RichTextBlock(
                                            label="Column body"
                                        )
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "activities",
                        wagtail.blocks.StructBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(label="Heading")),
                                (
                                    "count",
                                    wagtail.blocks.IntegerBlock(
                                        default=5, label="Count"
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "accordion_list",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "list_title",
                                    wagtail.blocks.CharBlock(
                                        help_text="Optional title for the list of accordions.",
                                        required=False,
                                    ),
                                ),
                                (
                                    "accordions",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "expand_accordion",
                                                    wagtail.blocks.BooleanBlock(
                                                        help_text="The accordion is collapsed by default. Select this option to have it expanded when the page loads.",
                                                        label="Expand accordion?",
                                                        required=False,
                                                    ),
                                                ),
                                                ("title", wagtail.blocks.CharBlock()),
                                                (
                                                    "body",
                                                    wagtail.blocks.RichTextBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        ),
                                        help_text="Add, remove, or reorder accordions.",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "infographic",
                        wagtail.blocks.StructBlock(
                            [
                                ("text_left", wagtail.blocks.CharBlock(max_length=50)),
                                (
                                    "text_center",
                                    wagtail.blocks.CharBlock(max_length=50),
                                ),
                                ("text_right", wagtail.blocks.CharBlock(max_length=50)),
                            ]
                        ),
                    ),
                    (
                        "map_teaser",
                        wagtail.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("body", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
    ]
