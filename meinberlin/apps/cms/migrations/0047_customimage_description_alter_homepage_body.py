# Generated by Django 4.2.11 on 2024-12-12 15:57

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_cms", "0046_alter_docspage_body"),
    ]

    operations = [
        migrations.AddField(
            model_name="customimage",
            name="description",
            field=models.CharField(
                blank=True, default="", max_length=255, verbose_name="description"
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("paragraph", 0),
                    ("call_to_action", 4),
                    ("image_call_to_action", 7),
                    ("columns_text", 11),
                    ("activities", 14),
                    ("accordion_list", 20),
                    ("infographic", 22),
                    ("map_teaser", 23),
                ],
                block_lookup={
                    0: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {"template": "meinberlin_cms/blocks/richtext_block.html"},
                    ),
                    1: ("wagtail.blocks.RichTextBlock", (), {}),
                    2: ("wagtail.blocks.CharBlock", (), {}),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Link Text", "max_length": 50},
                    ),
                    4: (
                        "wagtail.blocks.StructBlock",
                        [[("body", 1), ("link", 2), ("link_text", 3)]],
                        {},
                    ),
                    5: ("wagtail.images.blocks.ImageBlock", [], {}),
                    6: ("wagtail.blocks.CharBlock", (), {"max_length": 80}),
                    7: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("image", 5),
                                ("title", 6),
                                ("body", 1),
                                ("link", 2),
                                ("link_text", 3),
                            ]
                        ],
                        {},
                    ),
                    8: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                (2, "Two columns"),
                                (3, "Three columns"),
                                (4, "Four columns"),
                            ]
                        },
                    ),
                    9: ("wagtail.blocks.RichTextBlock", (), {"label": "Column body"}),
                    10: ("wagtail.blocks.ListBlock", (9,), {}),
                    11: (
                        "wagtail.blocks.StructBlock",
                        [[("columns_count", 8), ("columns", 10)]],
                        {},
                    ),
                    12: ("wagtail.blocks.CharBlock", (), {"label": "Heading"}),
                    13: (
                        "wagtail.blocks.IntegerBlock",
                        (),
                        {"default": 5, "label": "Count"},
                    ),
                    14: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 12), ("count", 13)]],
                        {},
                    ),
                    15: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Optional title for the list of accordions.",
                            "required": False,
                        },
                    ),
                    16: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "help_text": "The accordion is collapsed by default. Select this option to have it expanded when the page loads.",
                            "label": "Expand accordion?",
                            "required": False,
                        },
                    ),
                    17: ("wagtail.blocks.RichTextBlock", (), {"required": False}),
                    18: (
                        "wagtail.blocks.StructBlock",
                        [[("expand_accordion", 16), ("title", 2), ("body", 17)]],
                        {},
                    ),
                    19: (
                        "wagtail.blocks.ListBlock",
                        (18,),
                        {"help_text": "Add, remove, or reorder accordions."},
                    ),
                    20: (
                        "wagtail.blocks.StructBlock",
                        [[("list_title", 15), ("accordions", 19)]],
                        {},
                    ),
                    21: ("wagtail.blocks.CharBlock", (), {"max_length": 50}),
                    22: (
                        "wagtail.blocks.StructBlock",
                        [[("text_left", 21), ("text_center", 21), ("text_right", 21)]],
                        {},
                    ),
                    23: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 5), ("body", 1)]],
                        {},
                    ),
                },
            ),
        ),
    ]
