# Generated by Django 4.2 on 2023-11-27 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("a4labels", "0003_labelalias"),
        ("a4modules", "0009_alter_module_blueprint_type"),
        ("meinberlin_topicprio", "0012_alter_topic_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
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
            model_name="topic",
            name="labels",
            field=models.ManyToManyField(
                related_name="%(app_label)s_%(class)s_label",
                to="a4labels.label",
                verbose_name="Labels",
            ),
        ),
    ]
