# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-19 14:54
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_plans", "0013_add_helptext_for_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="cost_string",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Cost"
            ),
        ),
    ]
