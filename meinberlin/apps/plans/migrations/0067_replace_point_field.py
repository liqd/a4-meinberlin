# Generated by Django 4.2.16 on 2025-02-19 15:54

import django.contrib.gis.db.models.fields

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_plans", "0066_plan_geos_point"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plan",
            name="point",
        ),
        migrations.AddField(
            model_name="plan",
            name="point",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True,
                null=True,
                srid=4326,
                verbose_name="Can your plan be located on the map?",
            ),
        ),
    ]
