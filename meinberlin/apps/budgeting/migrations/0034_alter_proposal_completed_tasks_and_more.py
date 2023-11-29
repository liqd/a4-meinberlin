# Generated by Django 4.2 on 2023-11-29 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_moderationtasks", "0002_alter_moderationtask_options"),
        ("a4modules", "0008_alter_module_blueprint_type"),
        ("a4labels", "0003_labelalias"),
        ("meinberlin_budgeting", "0033_alter_proposal_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proposal",
            name="completed_tasks",
            field=models.ManyToManyField(
                related_name="%(app_label)s_%(class)s_completed",
                to="meinberlin_moderationtasks.moderationtask",
                verbose_name="completed moderation tasks",
            ),
        ),
        migrations.AlterField(
            model_name="proposal",
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
            model_name="proposal",
            name="labels",
            field=models.ManyToManyField(
                related_name="%(app_label)s_%(class)s_label",
                to="a4labels.label",
                verbose_name="Labels",
            ),
        ),
    ]
