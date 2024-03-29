# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 09:58
from __future__ import unicode_literals

from django.db import migrations

import adhocracy4.images.fields


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_mapideas", "0016_add_verbose_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mapidea",
            name="image",
            field=adhocracy4.images.fields.ConfiguredImageField(
                "idea_image",
                blank=True,
                help_prefix="Visualize your idea.",
                upload_to="ideas/images",
                verbose_name="Add image",
            ),
        ),
    ]
