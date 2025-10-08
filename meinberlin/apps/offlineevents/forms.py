from django import forms
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.components.forms import ModuleDashboardForm
from adhocracy4.forms.fields import DateTimeField
from django_ckeditor_5.fields import CKEditor5Field
from django_ckeditor_5.widgets import CKEditor5Widget


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


class OfflineEventSettingsForm(ModuleDashboardForm):
    event_date = DateTimeField(
        time_format="%H:%M",
        required=True,
        require_all_fields=False,
        label=(_("Date"), _("Time")),
    )

    def __init__(self, *args, **kwargs):
        self.module = kwargs["instance"]
        settings_instance = getattr(self.module, "settings_instance", None)
        kwargs["instance"] = settings_instance
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        super().save(commit)
        return self.module

    def get_project(self):
        return self.module.project

    class Meta:
        model = models.OfflineEventSettings
        fields = ["event_date"]
        required_for_project_publish = []


class OfflineEventBasicForm(ModuleDashboardForm):
    class Meta:
        from adhocracy4.modules import models as module_models
        model = models.OfflineEventSettings
        fields = ["event_type","name", "description"] # description wird als CKEditor5Field überschrieben
        required_for_project_publish = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings_instance = getattr(self.instance, "settings_instance", None)
        if settings_instance and settings_instance.event_type is not None:
            self.fields["event_type"].initial = settings_instance.event_type

    def save(self, commit=True):
        module = super().save(commit)
        settings_instance = getattr(module, "settings_instance", None)
        if settings_instance:
            settings_instance.event_type = self.cleaned_data.get("event_type")
            settings_instance.save(update_fields=["event_type"])
        return module
