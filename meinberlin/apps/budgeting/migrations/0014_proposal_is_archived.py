# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 14:13
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_budgeting", "0013_alter_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="proposal",
            name="is_archived",
            field=models.BooleanField(
                default=False,
                help_text="Exclude this proposal from all listings by default. You can still access this proposal by using filters.",
                verbose_name="Proposal is archived",
            ),
        ),
    ]
