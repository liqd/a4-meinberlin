# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-17 14:33
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_maps", "0003_auto_20170420_1321"),
        ("meinberlin_plans", "0004_remove_plan_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="district",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="meinberlin_maps.MapPreset",
            ),
        ),
    ]
