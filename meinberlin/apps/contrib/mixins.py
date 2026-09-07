from django import forms
from django.core import validators
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from rest_framework.response import Response

from adhocracy4.categories.models import CategoryAlias
from adhocracy4.labels.models import LabelAlias
from meinberlin.apps.contrib import fields
from meinberlin.apps.contrib import widgets

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


class ContactInfoFormMixin:
    """Add the contact information fields to an idea/proposal form.

    Expects the form's ``Meta.fields`` to include ``allow_contact``,
    ``contact_email`` and ``contact_phone``. An optional ``user`` keyword
    argument may be passed to offer the user's account e-mail address as a
    choice.
    """

    class Media:
        js = ("contact_information.js",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["allow_contact"].label = _(
            "For questions or in case of implementation "
            "of my proposal you can contact me. I will "
            "receive automatic notifications for any "
            "status update or official statement to my "
            "proposal."
        )
        self.fields["contact_phone"].label = _("Telephone number")
        self.fields["contact_storage_consent"] = forms.BooleanField(
            required=False, label=_("Contact storage consent")
        )
        if self.instance.allow_contact and self.instance.contact_email != "":
            self.initial["contact_storage_consent"] = True
        if user is not None and user.email:
            choices = [
                (
                    user.email,
                    _(
                        "Please contact me via the e-mail address "
                        "of my user account ({})."
                    ).format(user.email),
                ),
                ("other", _("Please contact me via another e-mail address:")),
            ]
            self.fields["contact_email"] = fields.ChoiceWithOtherOptionField(
                required=False,
                label=_("E-mail address"),
                choices=choices,
                widget=widgets.RadioSelectWithTextInputWidget(choices=choices),
                validators_textinput=[validators.validate_email],
            )
        else:
            self.fields["contact_email"].label = _("E-mail address")

    def clean(self):
        cleaned_data = super().clean()
        allow_contact = cleaned_data.get("allow_contact")
        contact_email = cleaned_data.get("contact_email")
        contact_storage_consent = cleaned_data.get("contact_storage_consent")
        if allow_contact:
            if not contact_email:
                self.add_error("contact_email", _("Please enter an email address."))
            if not contact_storage_consent:
                self.add_error(
                    "contact_storage_consent",
                    _("Please consent to the storage of your contact information."),
                )
        else:
            # keep the stored contact data consistent with the user's choice
            cleaned_data["contact_email"] = ""
            cleaned_data["contact_phone"] = ""
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
