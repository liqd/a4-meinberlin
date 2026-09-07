from django import forms
from django.utils.translation import gettext_lazy as _

from meinberlin.apps.mapideas.forms import MapIdeaForm
from meinberlin.apps.moderationtasks.mixins import TasksAddableFieldMixin

from . import models


class ProposalForm(MapIdeaForm):
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


class ProposalModerateForm(TasksAddableFieldMixin, forms.ModelForm):
    class Meta:
        model = models.Proposal
        fields = ["moderator_status", "is_archived", "completed_tasks"]
