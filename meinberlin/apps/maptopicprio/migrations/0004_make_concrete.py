# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 13:24
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_maptopicprio', '0003_alter_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maptopic',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
