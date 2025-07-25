from django import forms
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from rest_framework.response import Response

from adhocracy4.categories.models import CategoryAlias
from adhocracy4.labels.models import LabelAlias

RIGHT_OF_USE_LABEL = _(
    "I hereby confirm that the copyrights for this "
    "photo are with me or that I have received "
    "rights of use from the author. I also confirm "
    "that the privacy rights of depicted third persons "
    "are not violated. "
)


class ImageRightOfUseMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["right_of_use"] = forms.BooleanField(
            required=False, label=RIGHT_OF_USE_LABEL
        )
        if self.instance.image:
            self.initial["right_of_use"] = True

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        right_of_use = cleaned_data.get("right_of_use")
        if image and not right_of_use:
            self.add_error(
                "right_of_use",
                _(
                    "You want to upload an image. "
                    "Please check that you have the "
                    "right of use for the image."
                ),
            )
        return cleaned_data


class ContactStorageConsentMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["contact_storage_consent"] = forms.BooleanField(
            required=False, label=_("contact storage " "consent")
        )
        if self.instance.allow_contact and not self.instance.contact_email == "":
            self.initial["contact_storage_consent"] = True

    def clean(self):
        cleaned_data = super().clean()
        allow_contact = cleaned_data.get("allow_contact")
        contact_storage_consent = cleaned_data.get("contact_storage_consent")
        if allow_contact and not contact_storage_consent:
            self.add_error(
                "contact_storage_consent",
                _("Please consent to the storage of your contact " "information."),
            )
        return cleaned_data


class CategoryAndLabelAliasMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category_alias = CategoryAlias.get_category_alias(self.module)
        if category_alias:
            self.fields["category"].help_text = category_alias.description
            self.fields["category"].label = category_alias.title

        label_alias = LabelAlias.get_label_alias(self.module)
        if label_alias:
            self.fields["labels"].help_text = label_alias.description
            self.fields["labels"].label = label_alias.title


class LocaleInfoMixin:
    """Add the current locale of the user to the API response"""

    def list(self, request: Request, *args, **kwargs) -> Response:
        response = super().list(request, args, kwargs)
        response.data["locale"] = get_language()
        return response


class MapPolygonMixin:
    """Add the map polygon to the API response"""

    def list(self, request: Request, *args, **kwargs) -> Response:
        response = super().list(request, args, kwargs)
        response.data["polygon"] = self.module.settings_instance.polygon
        return response
