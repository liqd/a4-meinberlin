# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-08 13:33
from __future__ import unicode_literals

from django.db import migrations

import adhocracy4.maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_mapideas", "0017_add_verbose_for_idea_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mapidea",
            name="point",
            field=adhocracy4.maps.fields.PointField(
                help_text="Click inside the marked area or type in an address to set the marker. A set marker can be dragged when pressed.",
                verbose_name="Where can your idea be located on a map?",
            ),
        ),
    ]
