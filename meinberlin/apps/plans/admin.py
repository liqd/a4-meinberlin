from django import forms
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django_ckeditor_5.widgets import CKEditor5Widget

from . import models


class PlanAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"].widget = CKEditor5Widget(
            config_name="collapsible-image-editor",
        )

    class Meta:
        model = models.Plan
        fields = "__all__"


@admin.register(models.Plan)
class PlanAdmin(GISModelAdmin):
    form = PlanAdminForm
    list_display = ("__str__", "organisation", "created")

    date_hierarchy = "created"
    search_fields = ("title",)
    readonly_fields = ("creator",)
    gis_widget_kwargs = {
        "attrs": {
            "default_zoom": 12,  # Configure zoom level
            "default_lon": 13.404954,
            "default_lat": 52.520008,
        }
    }
