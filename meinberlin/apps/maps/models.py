from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.maps import fields as map_fields
from adhocracy4.modules import models as module_models


class MapPresetCategory(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MapPreset(models.Model):
    name = models.CharField(max_length=128)
    polygon = map_fields.MultiPolygonField()
    category = models.ForeignKey(
        MapPresetCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MapLayer(models.Model):
    """A map layer from an external geo service (WMS, optionally WFS)."""

    slug = models.SlugField(
        max_length=128,
        unique=True,
        verbose_name=_("Identifier"),
        help_text=_("Stable identifier, used to reference the layer."),
    )
    name = models.CharField(max_length=128, verbose_name=_("Name"))
    url = models.URLField(max_length=500, verbose_name=_("Service URL"))
    layer_name = models.CharField(max_length=255, verbose_name=_("Layer name"))
    attribution = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Attribution"),
    )
    opacity = models.FloatField(
        default=0.7,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        verbose_name=_("Opacity"),
    )
    wfs_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_("Vector service URL"),
        help_text=_("Optional WFS endpoint to render the layer as vector data."),
    )
    wfs_layer_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Vector layer name"),
        help_text=_("Feature type of the WFS request."),
    )
    wfs_property = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_("Vector style property"),
        help_text=_("Attribute used to colour the vector features."),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        ordering = ["order", "name"]
        verbose_name = _("Map layer")
        verbose_name_plural = _("Map layers")

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.pk,
            "name": self.name,
            "url": self.url,
            "layer": self.layer_name,
            "attribution": self.attribution,
            "opacity": self.opacity,
            "wfsUrl": self.wfs_url,
            "wfsLayer": self.wfs_layer_name,
            "wfsProperty": self.wfs_property,
        }


class ModuleMapLayer(models.Model):
    """Map layer selection for a single module."""

    module = models.OneToOneField(
        module_models.Module,
        on_delete=models.CASCADE,
        related_name="map_layer_selection",
    )
    layers = models.ManyToManyField(
        MapLayer,
        blank=True,
        related_name="module_selections",
    )

    class Meta:
        verbose_name = _("Module map layer selection")
        verbose_name_plural = _("Module map layer selections")

    def __str__(self):
        return f"Map layers for {self.module}"
