import pytest
from django.template.loader import render_to_string
from django.utils import translation

from meinberlin.apps.maps.dashboard import ExtendedAreaSettingsForm
from meinberlin.apps.maps.models import MapLayer

TEMPLATE = "a4dashboard/includes/module_areasettings_form.html"


class FakeView:
    def __init__(self, module):
        self.module = module


def render_form(module):
    form = ExtendedAreaSettingsForm(instance=module)
    with translation.override("en"):
        return render_to_string(TEMPLATE, {"form": form, "view": FakeView(module)})


@pytest.mark.django_db
def test_template_renders_empty_state(module, area_settings_factory):
    area_settings_factory(module=module)
    html = render_form(module)

    assert "No map layer has been added yet." in html
    assert "No map layer" in html
    assert 'id="map-layer-add-modal"' in html
    assert 'id="map-layer-edit-modal"' in html
    assert 'id="map-layer-delete-modal"' in html


@pytest.mark.django_db
def test_template_renders_layers_and_marks_active(module, area_settings_factory):
    area_settings_factory(module=module)
    MapLayer.objects.create(
        module=module,
        name="Straßenbäume",
        service_url="https://gdi.berlin.de/services/wms/baumbestand",
        layer_name="strassenbaeume",
        title="Straßenbäume",
        is_active=True,
    )
    MapLayer.objects.create(
        module=module,
        name="Anlagenbäume",
        service_url="https://gdi.berlin.de/services/wms/baumbestand",
        layer_name="anlagenbaeume",
        title="Anlagenbäume",
        is_active=False,
        is_available=False,
    )

    html = render_form(module)

    assert "Straßenbäume" in html
    assert "Anlagenbäume" in html
    assert "gdi.berlin.de/services/wms/baumbestand" in html
    assert "This map layer could not be loaded." in html
    # Only the active layer and the "none" option are preselected.
    assert html.count("checked") == 1
