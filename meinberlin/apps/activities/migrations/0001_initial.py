# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-25 12:44
from __future__ import unicode_literals

import autoslug.fields
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("a4modules", "0004_description_maxlength_512"),
    ]

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="a4modules.Item",
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                ("name", models.CharField(max_length=120, verbose_name="Title")),
                (
                    "highlight",
                    models.CharField(max_length=120, verbose_name="Highlighted Info"),
                ),
                (
                    "description",
                    models.TextField(verbose_name="Description"),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("a4modules.item",),
        ),
    ]
