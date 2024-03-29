# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-15 16:25
from __future__ import unicode_literals

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations

import meinberlin.apps.cms.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_cms", "0030_add_infographic_block"),
    ]

    operations = [
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
                        "projects",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(max_length=80)),
                                (
                                    "projects",
                                    wagtail.blocks.ListBlock(
                                        meinberlin.apps.cms.blocks.ProjectSelectionBlock(
                                            label="Project"
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
                        "accordion",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock()),
                                ("body", wagtail.blocks.RichTextBlock(required=False)),
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
                                ("icon", wagtail.blocks.RichTextBlock()),
                                ("title", wagtail.blocks.CharBlock()),
                                ("body", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    ),
                ]
            ),
        ),
    ]
