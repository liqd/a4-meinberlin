# Generated by Django 2.2.24 on 2021-09-27 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_cms", "0035_remove_project_block_from_homepage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storefrontitem",
            name="project",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"in_id": [1, 2]},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="a4projects.Project",
            ),
        ),
    ]
