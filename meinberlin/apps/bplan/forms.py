from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from meinberlin.apps.extprojects.forms import ExternalProjectCreateForm
from meinberlin.apps.extprojects.forms import ExternalProjectForm

from ..captcha.fields import CaptcheckCaptchaField
from . import models


class StatementForm(forms.ModelForm):
    captcha = CaptcheckCaptchaField(label=_("I am not a robot"))

    class Meta:
        model = models.Statement
        fields = ["name", "email", "statement", "street_number", "postal_code_city"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (hasattr(settings, "CAPTCHA_URL") and settings.CAPTCHA_URL):
            del self.fields["captcha"]


class BplanProjectCreateForm(ExternalProjectCreateForm):
    class Meta:
        model = models.Bplan
        fields = [
            "name",
            "description",
            "tile_image",
            "tile_image_alt_text",
            "tile_image_copyright",
        ]


class BplanProjectForm(ExternalProjectForm):
    administrative_district = forms.CharField(
        required=False,
        label=_("Administrative district"),
        help_text=_("Enter district short code (e.g., 'mi' for Mitte)"),
    )

    class Meta:
        model = models.Bplan
        fields = [
            "name",
            "url",
            "description",
            "tile_image",
            "tile_image_alt_text",
            "tile_image_copyright",
            "office_worker_email",
            "start_date",
            "end_date",
        ]
        required_for_project_publish = [
            "name",
            "url",
            "description",
            "office_worker_email",
            "start_date",
            "end_date",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"autocomplete": "off", "autofill": "off"}
        )
        # Set initial value to short code if instance has a district
        if self.instance and self.instance.administrative_district:
            self.initial["administrative_district"] = (
                self.instance.administrative_district.short_code
            )

    def clean_administrative_district(self):
        short_code = self.cleaned_data.get("administrative_district")
        print(f"DEBUG: short_code = {short_code}")
        if short_code:
            try:
                district = AdministrativeDistrict.objects.get(short_code=short_code)
                print(f"DEBUG: Found district = {district}, id = {district.id}")
                return district
            except AdministrativeDistrict.DoesNotExist:
                raise forms.ValidationError(
                    f"District with short code '{short_code}' not found."
                )
        print("DEBUG: short_code is empty or None")
        return None

    def save(self, commit=True):
        district = self.cleaned_data.get("administrative_district")

        if district is not None:
            self.instance.administrative_district = district

        project = super().save(commit)

        return project
