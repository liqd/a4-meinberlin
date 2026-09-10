from django import forms
from django.core import validators
from django.utils.translation import gettext_lazy as _

from adhocracy4.projects.guest_users import is_guest_user
from meinberlin.apps.contrib import fields
from meinberlin.apps.contrib import widgets
from meinberlin.apps.contrib.mixins import ContactStorageConsentMixin
from meinberlin.apps.mapideas.forms import MapIdeaForm
from meinberlin.apps.moderationtasks.mixins import TasksAddableFieldMixin

from . import models


class ProposalForm(ContactStorageConsentMixin, MapIdeaForm):
    class Meta:
        model = models.Proposal
        fields = [
            "name",
            "description",
            "image",
            "category",
            "labels",
            "budget",
            "point",
            "point_label",
            "allow_contact",
            "contact_email",
            "contact_phone",
        ]
        labels = {
            "allow_contact": _(
                "For questions or in case of implementation "
                "of my proposal you can contact me. I will "
                "receive automatic notifications for any "
                "status update or official statement to my "
                "proposal."
            ),
            "contact_phone": _("Telephone number"),
        }
        help_texts = {
            "category": _(
                "Assign your proposal to a category. This "
                "automatically appears in the display of your "
                "proposal. The list of all proposals can be "
                "filtered by category."
            ),
            "labels": _(
                "Specify your proposal with one or more labels. "
                "These will automatically appear in the display of "
                "your proposal. In addition, the list of all "
                "proposals can be filtered by labels."
            ),
        }

    class Media:
        js = ("budgeting_disable_contact.js",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and is_guest_user(user):
            # Guests have a throwaway account address (guest+...@liqd.net)
            # which must never be used as contact address. Show an empty
            # input instead of offering their account email for selection.
            self.fields["contact_email"] = forms.EmailField(
                required=False,
                label=_("E-mail address"),
            )
            # Guests do not receive automatic notifications; only the
            # official statement is sent to the entered contact email.
            self.fields["allow_contact"].label = _(
                "For questions or in case of implementation of my proposal "
                "you can contact me. I will receive the official statement "
                "on my proposal by email. As a guest I will not receive "
                "automatic notifications – for that, I can convert my guest "
                "account into a regular account."
            )
            return

        choices = [
            (
                user.email,
                _(
                    "Please contact me via the e-mail address of my user account ({})."
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

    def clean(self):
        cleaned_data = super().clean()
        allow_contact = cleaned_data.get("allow_contact")
        contact_email = cleaned_data.get("contact_email")
        if allow_contact and not contact_email:
            self.add_error("contact_email", _("Please enter an email address."))
        return cleaned_data


class ProposalModerateForm(TasksAddableFieldMixin, forms.ModelForm):
    class Meta:
        model = models.Proposal
        fields = ["moderator_status", "is_archived", "completed_tasks"]
