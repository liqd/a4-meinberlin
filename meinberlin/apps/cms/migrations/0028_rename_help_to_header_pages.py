# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-07 13:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_cms', '0027_helppages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HelpPages',
            new_name='HeaderPages',
        ),
    ]
