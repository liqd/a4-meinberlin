from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.maps import fields as map_fields


class MapLayer(models.Model):
    """A WMS layer from GDI Berlin, configured for a single module."""

    module = models.ForeignKey(
        "a4modules.Module",
        on_delete=models.CASCADE,
        related_name="map_layers",
    )
    name = models.CharField(max_length=200)
    service_url = models.URLField(max_length=500)
    layer_name = models.CharField(max_length=255)
    title = models.CharField(max_length=500, blank=True)
    attribution = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    last_checked_at = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created", "pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["module", "service_url", "layer_name"],
                name="unique_map_layer_per_module",
            )
        ]
        verbose_name = _("Map layer")
        verbose_name_plural = _("Map layers")

    def __str__(self):
        return f"{self.name} ({self.layer_name})"

    @property
    def key(self):
        return f"{self.service_url}|{self.layer_name}"


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
