# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-13 11:14
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0008_alter_user_username_max_length"),
        ("meinberlin_plans", "0038_change_ongoing_display_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="auth.Group",
            ),
        ),
    ]
