# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 09:58
from __future__ import unicode_literals

import autoslug.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations
from django.db import models

import adhocracy4.maps.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.A4_ORGANISATIONS_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("a4projects", "0013_help_texts"),
    ]

    operations = [
        migrations.CreateModel(
            name="Plan",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
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
                    models.DateTimeField(blank=True, editable=False, null=True),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="title", unique=True
                    ),
                ),
                ("title", models.CharField(max_length=120, verbose_name="Title")),
                (
                    "point",
                    adhocracy4.maps.fields.PointField(
                        help_text="Click inside marked area on the map to set a marker. Drag and drop the marker to change its place. Alternatively you can use the search field to search for an address.",
                        verbose_name="Where can the plan be located on a map?",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.A4_ORGANISATIONS_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="a4projects.Project",
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
    ]
