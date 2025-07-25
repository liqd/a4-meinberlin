# Generated by Django 4.2.16 on 2025-03-06 08:21

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_cms", "0046_remove_storefrontcollection_parent_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("paragraph", 0),
                    ("project", 6),
                    ("projects", 9),
                    ("user_action_bar", 17),
                    ("icon_list", 23),
                    ("columns_text", 27),
                    ("activities", 30),
                    ("accordion_list", 37),
                    ("teaser", 43),
                    ("info_bar", 46),
                ],
                block_lookup={
                    0: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {"template": "meinberlin_cms/blocks/richtext_block.html"},
                    ),
                    1: ("wagtail.blocks.CharBlock", (), {"max_length": 100}),
                    2: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Will be shown instead of the project title if set.",
                            "label": "Overwrite title",
                            "max_length": 100,
                            "required": False,
                        },
                    ),
                    3: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "help_text": "Will be shown instead of the project teaser if set.",
                            "label": "Overwrite teaser text",
                            "max_length": 250,
                            "required": False,
                        },
                    ),
                    4: (
                        "meinberlin.apps.cms.blocks.ProjectSelectionBlock",
                        (),
                        {"label": "Project"},
                    ),
                    5: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"default": "Show project", "max_length": 64},
                    ),
                    6: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("headline", 1),
                                ("custom_title", 2),
                                ("custom_teaser", 3),
                                ("project", 4),
                                ("button_text", 5),
                            ]
                        ],
                        {"label": "Project teaser"},
                    ),
                    7: ("wagtail.blocks.CharBlock", (), {"max_length": 80}),
                    8: ("wagtail.blocks.ListBlock", (4,), {"min_num": 3}),
                    9: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 7), ("projects", 8)]],
                        {},
                    ),
                    10: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "help_text": "Use '%username%' in the text to display the username",
                            "label": "Body",
                        },
                    ),
                    11: ("wagtail.blocks.CharBlock", (), {"required": True}),
                    12: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {
                            "help_text": "Please enter a full url which starts with https://",
                            "max_length": 500,
                            "required": True,
                        },
                    ),
                    13: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("light", "light"),
                                ("fulltone", "fulltone"),
                                ("primary", "primary"),
                            ]
                        },
                    ),
                    14: (
                        "wagtail.blocks.StructBlock",
                        [[("link_text", 11), ("link", 12), ("style", 13)]],
                        {},
                    ),
                    15: ("wagtail.blocks.ListBlock", (14,), {"label": "Buttons"}),
                    16: ("wagtail.blocks.RichTextBlock", (), {"label": "Body"}),
                    17: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("body_logged_in", 10),
                                ("buttons_logged_in", 15),
                                ("body_anonymous", 16),
                                ("buttons_anonymous", 15),
                            ]
                        ],
                        {},
                    ),
                    18: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Optional title for the list of panels.",
                            "required": False,
                        },
                    ),
                    19: ("wagtail.images.blocks.ImageBlock", [], {}),
                    20: ("wagtail.blocks.RichTextBlock", (), {}),
                    21: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 19), ("body", 20)]],
                        {},
                    ),
                    22: ("wagtail.blocks.ListBlock", (21,), {}),
                    23: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 18), ("icon_list_blocks", 22)]],
                        {},
                    ),
                    24: (
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
                    25: ("wagtail.blocks.RichTextBlock", (), {"label": "Column body"}),
                    26: ("wagtail.blocks.ListBlock", (25,), {}),
                    27: (
                        "wagtail.blocks.StructBlock",
                        [[("columns_count", 24), ("columns", 26)]],
                        {},
                    ),
                    28: ("wagtail.blocks.CharBlock", (), {"label": "Heading"}),
                    29: (
                        "wagtail.blocks.IntegerBlock",
                        (),
                        {"default": 5, "label": "Count"},
                    ),
                    30: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 28), ("count", 29)]],
                        {},
                    ),
                    31: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Optional title for the list of accordions.",
                            "required": False,
                        },
                    ),
                    32: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "help_text": "The accordion is collapsed by default. Select this option to have it expanded when the page loads.",
                            "label": "Expand accordion?",
                            "required": False,
                        },
                    ),
                    33: ("wagtail.blocks.CharBlock", (), {}),
                    34: ("wagtail.blocks.RichTextBlock", (), {"required": False}),
                    35: (
                        "wagtail.blocks.StructBlock",
                        [[("expand_accordion", 32), ("title", 33), ("body", 34)]],
                        {},
                    ),
                    36: (
                        "wagtail.blocks.ListBlock",
                        (35,),
                        {"help_text": "Add, remove, or reorder accordions."},
                    ),
                    37: (
                        "wagtail.blocks.StructBlock",
                        [[("list_title", 31), ("accordions", 36)]],
                        {},
                    ),
                    38: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [("left", "Left"), ("right", "Right")],
                            "help_text": "Should the image be on the left or on the right?",
                        },
                    ),
                    39: ("wagtail.blocks.CharBlock", (), {"max_length": 70}),
                    40: ("wagtail.blocks.RichTextBlock", (), {"max_length": 250}),
                    41: (
                        "wagtail.blocks.StructBlock",
                        [[("link_text", 11), ("link", 12), ("style", 13)]],
                        {"form_classname": "w-field w-panel", "required": False},
                    ),
                    42: (
                        "wagtail.images.blocks.ImageBlock",
                        [],
                        {"form_classname": "w-field w-panel"},
                    ),
                    43: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("alignment", 38),
                                ("title", 39),
                                ("body", 40),
                                ("button", 41),
                                ("image", 42),
                            ]
                        ],
                        {},
                    ),
                    44: ("wagtail.blocks.PageChooserBlock", (), {"required": True}),
                    45: (
                        "wagtail.blocks.StructBlock",
                        [[("link_text", 11), ("link", 44)]],
                        {"form_classname": "w-field w-panel", "required": False},
                    ),
                    46: (
                        "wagtail.blocks.StructBlock",
                        [[("body", 20), ("image", 42), ("link", 45)]],
                        {},
                    ),
                },
            ),
        ),
    ]
