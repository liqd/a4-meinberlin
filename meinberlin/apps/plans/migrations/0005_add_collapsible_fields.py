# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-11 15:42
from __future__ import unicode_literals

from django.db import migrations
import meinberlin.apps.ckeditor_collapsible.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_plans', '0004_remove_plan_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='description',
            field=meinberlin.apps.ckeditor_collapsible.fields.RichTextCollapsibleField(blank=True, verbose_name='Description'),
        ),
    ]
