from django.contrib import admin

from . import models


@admin.register(models.MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "layer_name", "order", "opacity")
    list_editable = ("order",)
    search_fields = ("name", "slug", "layer_name")


admin.site.register(models.MapPreset, admin.ModelAdmin)
admin.site.register(models.MapPresetCategory, admin.ModelAdmin)
admin.site.register(models.ModuleMapLayer, admin.ModelAdmin)
