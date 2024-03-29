# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-22 10:45
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations
from django.db import models


def delete_plans(apps, schema_editor):
    plan_model = apps.get_model("meinberlin_plans", "Plan")
    for plan in plan_model.objects.all():
        plan.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_plans", "0005_plan_district"),
    ]

    operations = [
        migrations.RunPython(delete_plans),
        migrations.AlterField(
            model_name="plan",
            name="district",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="meinberlin_maps.MapPreset",
            ),
        ),
    ]
