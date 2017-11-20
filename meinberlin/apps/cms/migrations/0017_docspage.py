# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('meinberlin_cms', '0016_attach_inline'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.StreamField((('documents_list', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('body', wagtail.wagtailcore.blocks.RichTextBlock(required=False))))),))),
                ('description', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Documents',
            },
            bases=('wagtailcore.page',),
        ),
    ]
