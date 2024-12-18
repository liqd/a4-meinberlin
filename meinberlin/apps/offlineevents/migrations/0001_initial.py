# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import autoslug.fields
import django.utils.timezone
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("a4projects", "0007_add_verbose_names"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OfflineEvent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        primary_key=True,
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, null=True, editable=False),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        unique=True, editable=False, populate_from="name"
                    ),
                ),
                ("name", models.CharField(verbose_name="Name", max_length=120)),
                (
                    "date",
                    models.DateTimeField(verbose_name="Date", blank=True, null=True),
                ),
                (
                    "description",
                    models.TextField(verbose_name="Description"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        to="a4projects.Project", on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
    ]
