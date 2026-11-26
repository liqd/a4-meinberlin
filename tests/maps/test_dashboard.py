import json
from unittest.mock import patch

import pytest

from adhocracy4.dashboard import components
from meinberlin.apps.maps import gdi_wms
from meinberlin.apps.maps.dashboard import ExtendedAreaSettingsForm
from meinberlin.apps.maps.models import MapLayer


def service_layers(layers):
    return {
        "service_url": "https://gdi.berlin.de/services/wms/baumbestand",
        "service_title": "Baumbestand Berlin",
        "version": "1.3.0",
        "format": "image/png",
        "layers": [
            {
                "name": layer["layer_name"],
                "title": layer["title"],
                "abstract": "",
                "attribution": layer["attribution"],
                "legend_url": "",
            }
            for layer in layers
        ],
    }


def form_data(polygon, layers, selected=""):
    return {
        "polygon": json.dumps(polygon),
        "map_layers": json.dumps(layers),
        "selected_map_layer": selected,
    }


@pytest.mark.django_db
def test_area_settings_component_uses_extended_form():
    component = components.modules.get("area_settings")
    assert component.form_class is ExtendedAreaSettingsForm
    assert component.form_template_name == (
        "a4dashboard/includes/module_areasettings_form.html"
    )


@pytest.mark.django_db
def test_saves_layers_with_area_settings(module, area_settings_factory):
    area_settings = area_settings_factory(module=module)
    layers = [
        {
            "name": "Straßenbäume",
            "service_url": "https://gdi.berlin.de/services/wms/baumbestand",
            "layer_name": "strassenbaeume",
            "title": "Straßenbäume",
            "attribution": "GDI Berlin",
            "is_available": True,
            "opacity": 40,
            "key": "https://gdi.berlin.de/services/wms/baumbestand|strassenbaeume",
        }
    ]
    selected = layers[0]["key"]

    with patch(
        "meinberlin.apps.maps.dashboard.gdi_wms.get_service_layers",
        return_value=service_layers(layers),
    ):
        form = ExtendedAreaSettingsForm(
            data=form_data(area_settings.polygon, layers, selected),
            instance=module,
        )
        assert form.is_valid(), form.errors
        form.save()

    saved = MapLayer.objects.get(module=module)
    assert saved.name == "Straßenbäume"
    assert saved.layer_name == "strassenbaeume"
    assert saved.is_active is True
    assert saved.opacity == 40


def test_opacity_is_clamped_and_snapped():
    clean = ExtendedAreaSettingsForm._clean_opacity
    assert clean({"opacity": 57}) == 60
    assert clean({"opacity": -5}) == 0
    assert clean({"opacity": 500}) == 100
    assert clean({}) == 100


@pytest.mark.django_db
def test_removing_the_active_layer_clears_selection(module, area_settings_factory):
    area_settings = area_settings_factory(module=module)
    MapLayer.objects.create(
        module=module,
        name="Straßenbäume",
        service_url="https://gdi.berlin.de/services/wms/baumbestand",
        layer_name="strassenbaeume",
        is_active=True,
    )

    form = ExtendedAreaSettingsForm(
        data=form_data(area_settings.polygon, [], ""),
        instance=module,
    )
    assert form.is_valid(), form.errors
    form.save()

    assert not MapLayer.objects.filter(module=module).exists()


@pytest.mark.django_db
def test_duplicate_layers_are_rejected(module, area_settings_factory):
    area_settings = area_settings_factory(module=module)
    layer = {
        "name": "Straßenbäume",
        "service_url": "https://gdi.berlin.de/services/wms/baumbestand",
        "layer_name": "strassenbaeume",
        "title": "Straßenbäume",
        "attribution": "GDI Berlin",
        "is_available": True,
        "key": "https://gdi.berlin.de/services/wms/baumbestand|strassenbaeume",
    }

    with patch(
        "meinberlin.apps.maps.dashboard.gdi_wms.get_service_layers",
        return_value=service_layers([layer]),
    ):
        form = ExtendedAreaSettingsForm(
            data=form_data(area_settings.polygon, [layer, layer]),
            instance=module,
        )
        assert not form.is_valid()
        assert "map_layers" in form.errors


@pytest.mark.django_db
def test_unreachable_service_is_saved_with_warning(module, area_settings_factory):
    area_settings = area_settings_factory(module=module)
    layer = {
        "name": "Straßenbäume",
        "service_url": "https://gdi.berlin.de/services/wms/baumbestand",
        "layer_name": "strassenbaeume",
        "title": "Straßenbäume",
        "attribution": "GDI Berlin",
        "is_available": True,
        "key": "https://gdi.berlin.de/services/wms/baumbestand|strassenbaeume",
    }

    with patch(
        "meinberlin.apps.maps.dashboard.gdi_wms.get_service_layers",
        side_effect=gdi_wms.MapLayerError("unreachable", "unreachable"),
    ):
        form = ExtendedAreaSettingsForm(
            data=form_data(area_settings.polygon, [layer], layer["key"]),
            instance=module,
        )
        assert form.is_valid(), form.errors
        form.save()

    saved = MapLayer.objects.get(module=module)
    assert saved.is_available is False
    assert saved.is_active is True


@pytest.mark.django_db
def test_unknown_selected_layer_is_cleared(module, area_settings_factory):
    area_settings = area_settings_factory(module=module)
    layer = {
        "name": "Straßenbäume",
        "service_url": "https://gdi.berlin.de/services/wms/baumbestand",
        "layer_name": "strassenbaeume",
        "title": "Straßenbäume",
        "attribution": "GDI Berlin",
        "is_available": True,
        "key": "https://gdi.berlin.de/services/wms/baumbestand|strassenbaeume",
    }

    with patch(
        "meinberlin.apps.maps.dashboard.gdi_wms.get_service_layers",
        return_value=service_layers([layer]),
    ):
        form = ExtendedAreaSettingsForm(
            data=form_data(
                area_settings.polygon,
                [layer],
                "https://gdi.berlin.de/services/wms/baumbestand|unknown",
            ),
            instance=module,
        )
        assert form.is_valid(), form.errors
        form.save()

    assert MapLayer.objects.get(module=module).is_active is False
