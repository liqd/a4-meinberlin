# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-21 14:24
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_extprojects", "0002_make_url_optional"),
    ]

    operations = [
        migrations.AlterField(
            model_name="externalproject",
            name="url",
            field=models.URLField(
                blank=True,
                help_text="Please enter a full url which starts with https:// or http://",
                verbose_name="URL",
            ),
        ),
    ]
