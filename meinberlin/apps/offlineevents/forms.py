from django import forms
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.components.forms import ModuleDashboardForm
from adhocracy4.forms.fields import DateTimeField

from . import models


class OfflineEventForm(forms.ModelForm):
    date = DateTimeField(
        time_format="%H:%M",
        required=True,
        require_all_fields=False,
        label=(_("Date"), _("Time")),
    )

    class Meta:
        model = models.OfflineEvent
        fields = ["name", "event_type", "date", "description"]
        help_texts = {
            "description": _(
                "If you add an image, please provide an alternate text. "
                "It serves as a textual description of the image content "
                "and is read out by screen readers. Describe the image "
                "in approx. 80 characters. Example: A busy square with "
                "people in summer."
            ),
            "event_type": _(
                "Please describe in no more than 30 characters the event "
                "type, e.g. Information event or 3rd public workshop."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].label = _("Date and time")


# Module Area


class OfflineEventItemForm(ModuleDashboardForm):
    event_date = DateTimeField(
        time_format="%H:%M",
        required=True,
        require_all_fields=False,
        label=(_("Date"), _("Time")),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.OfflineEventItem
        fields = ["event_date"]
        required_for_project_publish = ["event_date"]


class OfflineEventBasicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["name"].label = _("Name of event")
        self.fields["event_type"].required = True
        self.fields["description"].required = True

    class Meta:
        from adhocracy4.modules import models as module_models

        model = models.OfflineEventItem
        fields = [
            "event_type",
            "name",
            "description",
        ]
        help_texts = {
            "description": _(
                "If you add an image, please provide an alternate text. "
                "It serves as a textual description of the image content "
                "and is read out by screen readers. Describe the image "
                "in approx. 80 characters. Example: A busy square with "
                "people in summer."
            ),
            "event_type": _(
                "Please describe in no more than 30 characters the event "
                "type, e.g. Information event or 3rd public workshop."
            ),
        }
        required_for_project_publish = "__all__"
