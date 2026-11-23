import json

from django import forms
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import components
from adhocracy4.dashboard.dashboard import ModuleAreaSettingsComponent
from adhocracy4.dashboard.forms import AreaSettingsForm

from . import gdi_wms
from .models import MapLayer
from .widgets import MapChoosePolygonWithPresetWidget

MAX_MAP_LAYERS = 30


class ExtendedAreaSettingsForm(AreaSettingsForm):
    map_layers = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )
    selected_map_layer = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )

    class Meta(AreaSettingsForm.Meta):
        widgets = {"polygon": MapChoosePolygonWithPresetWidget}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["map_layers"].initial = json.dumps(
            self.get_map_layer_rows(), ensure_ascii=False
        )
        self.fields["selected_map_layer"].initial = self.get_selected_map_layer_key()

    def get_map_layer_rows(self):
        raw_layers = None
        if self.is_bound:
            raw_layers = self.data.get(self.add_prefix("map_layers"))

        if raw_layers is not None:
            try:
                layers = json.loads(raw_layers)
            except (TypeError, ValueError):
                return []
            if isinstance(layers, list):
                return [layer for layer in layers if isinstance(layer, dict)]
            return []

        return [
            {
                "name": layer.name,
                "service_url": layer.service_url,
                "layer_name": layer.layer_name,
                "title": layer.title,
                "attribution": layer.attribution,
                "is_available": layer.is_available,
                "key": layer.key,
            }
            for layer in self.module.map_layers.all()
        ]

    def get_selected_map_layer_key(self):
        if self.is_bound:
            return self.data.get(self.add_prefix("selected_map_layer"), "")
        selected = self.module.map_layers.filter(is_active=True).first()
        return selected.key if selected else ""

    def clean_map_layers(self):
        layers = self._parse_map_layers()
        seen = set()
        return [self._clean_layer(layer, seen) for layer in layers]

    def _parse_map_layers(self):
        raw_layers = self.cleaned_data.get("map_layers") or "[]"
        try:
            layers = json.loads(raw_layers)
        except (TypeError, ValueError):
            raise forms.ValidationError(_("The map layers could not be read."))

        if not isinstance(layers, list):
            raise forms.ValidationError(_("The map layers could not be read."))
        if len(layers) > MAX_MAP_LAYERS:
            raise forms.ValidationError(
                _("You can add at most %(count)s map layers.")
                % {"count": MAX_MAP_LAYERS}
            )
        return layers

    def _clean_layer(self, layer_data, seen):
        if not isinstance(layer_data, dict):
            raise forms.ValidationError(_("The map layers could not be read."))

        service_url = str(layer_data.get("service_url", "")).strip()
        layer_name = str(layer_data.get("layer_name", "")).strip()
        if not layer_name:
            raise forms.ValidationError(
                _("Please select a layer for every map service.")
            )

        try:
            service_id = gdi_wms.parse_service_id(service_url)
        except gdi_wms.MapLayerError as error:
            raise forms.ValidationError(error.message)

        try:
            service = gdi_wms.get_service_layers(service_id)
        except gdi_wms.MapLayerError as error:
            if error.code != "unreachable":
                raise forms.ValidationError(error.message)
            return self._unavailable_layer(layer_data, service_id, layer_name, seen)

        layer = next(
            (
                candidate
                for candidate in service["layers"]
                if candidate["name"] == layer_name
            ),
            None,
        )
        if layer is None:
            raise forms.ValidationError(_("The selected map layer is not available."))

        key = f"{service['service_url']}|{layer_name}"
        if key in seen:
            raise forms.ValidationError(_("This map layer has already been added."))
        seen.add(key)

        name = str(layer_data.get("name", "")).strip() or layer["title"]
        return {
            "name": name[:200],
            "service_url": service["service_url"],
            "layer_name": layer_name[:255],
            "title": layer["title"][:500],
            "attribution": layer["attribution"][:500],
            "is_available": True,
            "last_checked_at": timezone.now(),
            "key": key,
        }

    def _unavailable_layer(self, layer_data, service_id, layer_name, seen):
        service_url = gdi_wms.service_url(service_id)
        key = f"{service_url}|{layer_name}"
        if key in seen:
            raise forms.ValidationError(_("This map layer has already been added."))
        seen.add(key)
        return {
            "name": (
                str(layer_data.get("name", "")).strip()
                or str(layer_data.get("title", "")).strip()
                or layer_name
            )[:200],
            "service_url": service_url,
            "layer_name": layer_name[:255],
            "title": str(layer_data.get("title", "")).strip()[:500],
            "attribution": str(layer_data.get("attribution", "")).strip()[:500],
            "is_available": False,
            "last_checked_at": timezone.now(),
            "key": key,
        }

    def clean(self):
        cleaned_data = super().clean()
        layers = cleaned_data.get("map_layers") or []
        selected = cleaned_data.get("selected_map_layer", "").strip()
        valid_keys = {layer["key"] for layer in layers}
        if selected and selected not in valid_keys:
            cleaned_data["selected_map_layer"] = ""
        return cleaned_data

    def save(self, commit=True):
        with transaction.atomic():
            module = super().save(commit=commit)
            if not commit:
                return module

            layers = self.cleaned_data.get("map_layers") or []
            selected = self.cleaned_data.get("selected_map_layer", "")
            module.map_layers.all().delete()
            for layer in layers:
                MapLayer.objects.create(
                    module=module,
                    name=layer["name"],
                    service_url=layer["service_url"],
                    layer_name=layer["layer_name"],
                    title=layer["title"],
                    attribution=layer["attribution"],
                    is_active=layer["key"] == selected,
                    is_available=layer["is_available"],
                    last_checked_at=layer["last_checked_at"],
                )
            return module


class ModuleExtendedAreaSettingsComponent(ModuleAreaSettingsComponent):
    form_class = ExtendedAreaSettingsForm


components.replace_module(ModuleExtendedAreaSettingsComponent())
