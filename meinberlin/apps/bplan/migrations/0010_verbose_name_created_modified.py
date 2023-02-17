# Generated by Django 3.2.18 on 2023-02-17 10:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_bplan", "0009_rm_statement_charlimit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="statement",
            name="created",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="Created",
            ),
        ),
        migrations.AlterField(
            model_name="statement",
            name="modified",
            field=models.DateTimeField(
                blank=True, editable=False, null=True, verbose_name="Modified"
            ),
        ),
    ]
