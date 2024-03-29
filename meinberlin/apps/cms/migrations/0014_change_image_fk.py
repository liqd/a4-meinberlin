# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-06 06:40
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations
from django.db import models


def set_custom_image_id(apps, schema_editor):
    CustomImage = apps.get_model("meinberlin_cms", "CustomImage")
    HomePages = apps.get_model("meinberlin_cms", "HomePage")

    for hp in HomePages.objects.all():
        if hp.header_image:
            image = hp.header_image
            hp.custom_image_id = CustomImage.objects.get(id=image.id)
            hp.save()


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_cms", "0013_copy_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="header_image",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="meinberlin_cms.CustomImage",
            ),
        ),
        migrations.RunPython(set_custom_image_id),
    ]
