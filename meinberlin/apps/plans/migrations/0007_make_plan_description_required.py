# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-20 13:06
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import TextField


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_plans", "0006_make_plan_district_required"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="description",
            field=TextField(verbose_name="Description"),
        ),
    ]
