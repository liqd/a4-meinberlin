# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 13:43
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_users", "0003_user_get_newsletters"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="get_notifications",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether you want to receive notifications about content you follow. Unselect if you do not want to receive notifications.",
                verbose_name="Send me email notifications",
            ),
        ),
    ]
