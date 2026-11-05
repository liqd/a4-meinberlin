import django.core.validators
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("a4modules", "__first__"),
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
                (
                    "slug",
                    models.SlugField(
                        help_text="Stable identifier, used to reference the layer.",
                        max_length=128,
                        unique=True,
                        verbose_name="Identifier",
                    ),
                ),
                ("name", models.CharField(max_length=128, verbose_name="Name")),
                (
                    "url",
                    models.URLField(max_length=500, verbose_name="Service URL"),
                ),
                (
                    "layer_name",
                    models.CharField(max_length=255, verbose_name="Layer name"),
                ),
                (
                    "attribution",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Attribution"
                    ),
                ),
                (
                    "opacity",
                    models.FloatField(
                        default=0.7,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                        verbose_name="Opacity",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(default=0, verbose_name="Order"),
                ),
            ],
            options={
                "verbose_name": "Map layer",
                "verbose_name_plural": "Map layers",
                "ordering": ["order", "name"],
            },
        ),
        migrations.CreateModel(
            name="ModuleMapLayer",
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
                (
                    "module",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="map_layer_selection",
                        to="a4modules.module",
                    ),
                ),
                (
                    "layers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="module_selections",
                        to="meinberlin_maps.maplayer",
                    ),
                ),
            ],
            options={
                "verbose_name": "Module map layer selection",
                "verbose_name_plural": "Module map layer selections",
            },
        ),
    ]
