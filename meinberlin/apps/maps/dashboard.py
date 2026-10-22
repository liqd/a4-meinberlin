from django import forms
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import components
from adhocracy4.dashboard.dashboard import ModuleAreaSettingsComponent
from adhocracy4.dashboard.forms import AreaSettingsForm

from .models import MapLayer
from .models import ModuleMapLayer
from .widgets import MapChoosePolygonWithPresetWidget


class ExtendedAreaSettingsForm(AreaSettingsForm):
    class Meta(AreaSettingsForm.Meta):
        widgets = {"polygon": MapChoosePolygonWithPresetWidget}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.module.blueprint_type != "MBS":
            return

        self.fields["layers"] = forms.ModelMultipleChoiceField(
            queryset=MapLayer.objects.all(),
            required=False,
            widget=forms.CheckboxSelectMultiple,
            label=_("Map layers"),
            help_text=_(
                "Select the map layers that should be shown on the "
                "participation map. Multiple layers can be combined."
            ),
        )

        selection = ModuleMapLayer.objects.filter(module=self.module).first()
        if selection:
            self.initial["layers"] = selection.layers.values_list("pk", flat=True)

        self.fields["polygon"].widget.layers = [
            layer.as_dict() for layer in MapLayer.objects.all()
        ]

    def save(self, commit=True):
        module = super().save(commit)
        if "layers" in self.fields:
            layers = self.cleaned_data.get("layers", [])
            if layers or ModuleMapLayer.objects.filter(module=self.module).exists():
                selection, _ = ModuleMapLayer.objects.get_or_create(module=self.module)
                selection.layers.set(layers)
                self.module.map_layer_selection = selection
        return module


class ModuleExtendedAreaSettingsComponent(ModuleAreaSettingsComponent):
    form_class = ExtendedAreaSettingsForm


components.replace_module(ModuleExtendedAreaSettingsComponent())
