# Generated by Django 4.2 on 2023-11-29 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("a4modules", "0008_alter_module_blueprint_type"),
        ("a4labels", "0003_labelalias"),
        ("meinberlin_maptopicprio", "0011_alter_maptopic_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="maptopic",
            name="item_ptr",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                related_name="%(app_label)s_%(class)s",
                serialize=False,
                to="a4modules.item",
            ),
        ),
        migrations.AlterField(
            model_name="maptopic",
            name="labels",
            field=models.ManyToManyField(
                related_name="%(app_label)s_%(class)s_label",
                to="a4labels.label",
                verbose_name="Labels",
            ),
        ),
    ]
