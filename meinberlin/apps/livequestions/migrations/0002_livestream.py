# Generated by Django 2.2.16 on 2020-11-06 15:46

from django.db import migrations, models
import django.db.models.deletion
from django.db.models import TextField


class Migration(migrations.Migration):

    dependencies = [
        ("a4modules", "0005_module_is_draft"),
        ("meinberlin_livequestions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LiveStream",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="a4modules.Item",
                    ),
                ),
                (
                    "live_stream",
                    TextField(blank=True, verbose_name="Live Stream"),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("a4modules.item",),
        ),
    ]
