# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-30 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_cms', '0024_update_storefront'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storefrontitem',
            name='quote',
            field=models.TextField(blank=True, max_length=150),
        ),
    ]
