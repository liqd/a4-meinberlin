# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_mapideas", "0005_update-strings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mapidea",
            name="description",
            field=ckeditor.fields.RichTextField(verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="mapidea",
            name="name",
            field=models.CharField(max_length=120, verbose_name="Name"),
        ),
    ]
