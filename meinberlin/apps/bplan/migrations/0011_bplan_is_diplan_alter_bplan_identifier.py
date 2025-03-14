# Generated by Django 4.2.11 on 2024-11-18 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_bplan", "0010_verbose_name_created_modified"),
    ]

    operations = [
        migrations.AddField(
            model_name="bplan",
            name="is_diplan",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="bplan",
            name="identifier",
            field=models.CharField(
                blank=True,
                help_text="The identifier has to be identical to the identifier in the FIS-Broker, so that district and location are added automatically.",
                max_length=120,
                verbose_name="Identifier",
            ),
        ),
    ]
