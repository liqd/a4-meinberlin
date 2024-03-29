# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 08:57
from __future__ import unicode_literals

from django.db import migrations

import adhocracy4.images.fields


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_topicprio", "0009_add_label_verbose_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="image",
            field=adhocracy4.images.fields.ConfiguredImageField(
                "idea_image",
                blank=True,
                upload_to="ideas/images",
                verbose_name="Add image",
            ),
        ),
    ]
