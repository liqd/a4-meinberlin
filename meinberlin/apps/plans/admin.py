from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from . import models


class PlanAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"].widget = CKEditorUploadingWidget(
            config_name="collapsible-image-editor",
        )

    class Meta:
        model = models.Plan
        fields = "__all__"


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    form = PlanAdminForm
    list_display = ("__str__", "organisation", "created")

    date_hierarchy = "created"
    search_fields = ("title",)
    readonly_fields = ("creator",)
