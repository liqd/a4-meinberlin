import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a4modules", "0010_populate_item_polymorphic_ctype"),
        ("meinberlin_maps", "0003_auto_20170420_1321"),
    ]

    operations = [
        migrations.CreateModel(
            name="MapLayer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("service_url", models.URLField(max_length=500)),
                ("layer_name", models.CharField(max_length=255)),
                ("title", models.CharField(blank=True, max_length=500)),
                ("attribution", models.CharField(blank=True, max_length=500)),
                ("is_active", models.BooleanField(default=False)),
                ("is_available", models.BooleanField(default=True)),
                ("last_checked_at", models.DateTimeField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="map_layers",
                        to="a4modules.module",
                    ),
                ),
            ],
            options={
                "verbose_name": "Map layer",
                "verbose_name_plural": "Map layers",
                "ordering": ["created", "pk"],
            },
        ),
        migrations.AddConstraint(
            model_name="maplayer",
            constraint=models.UniqueConstraint(
                fields=("module", "service_url", "layer_name"),
                name="unique_map_layer_per_module",
            ),
        ),
    ]
