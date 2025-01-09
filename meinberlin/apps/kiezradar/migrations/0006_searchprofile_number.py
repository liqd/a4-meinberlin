# Generated by Django 4.2.11 on 2025-01-09 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_kiezradar", "0005_populate_project_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchprofile",
            name="number",
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddIndex(
            model_name="searchprofile",
            index=models.Index(models.F("number"), name="searchprofile_number_idx"),
        ),
        migrations.AlterModelOptions(
            name="searchprofile",
            options={"ordering": ["number"]},
        ),
        migrations.AlterField(
            model_name="searchprofile",
            name="name",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
