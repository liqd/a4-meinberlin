import html
import json
import re

import pytest

from adhocracy4.test.helpers import render_template
from meinberlin.apps.mapideas.templatetags.react_mapideas import get_map_layers
from meinberlin.apps.maps.dashboard import ExtendedAreaSettingsForm
from meinberlin.apps.maps.models import MapLayer
from meinberlin.apps.maps.models import ModuleMapLayer


def create_layer(**kwargs):
    defaults = {
        "slug": "test-layer",
        "name": "Test layer",
        "url": "https://example.org/wms",
        "layer_name": "test_layer",
        "attribution": "© Test",
        "opacity": 0.7,
        "order": 1,
    }
    defaults.update(kwargs)
    return MapLayer.objects.create(**defaults)


def get_rendered_props(context, template):
    rendered_template = render_template(template, context)
    expected = (
        r"^<div data-mb-widget=\"map-ideas\" data-attributes="
        r"\"(?P<props>{.+})\"><\/div>$"
    )
    match = re.match(expected, rendered_template)
    return json.loads(html.unescape(match.group("props")))


@pytest.mark.django_db
def test_map_layers_are_saved_for_spatial_brainstorming(
    module_factory, area_settings_factory
):
    module = module_factory(blueprint_type="MBS")
    area_settings_factory(module=module)
    layer = create_layer()

    form = ExtendedAreaSettingsForm(
        data={
            "polygon": json.dumps(module.settings_instance.polygon),
            "layers": [layer.pk],
        },
        instance=module,
    )

    assert form.is_valid(), form.errors
    form.save()

    assert list(module.map_layer_selection.layers.all()) == [layer]


@pytest.mark.django_db
def test_map_layers_can_be_cleared(module_factory, area_settings_factory):
    module = module_factory(blueprint_type="MBS")
    area_settings_factory(module=module)
    layer = create_layer()
    selection = ModuleMapLayer.objects.create(module=module)
    selection.layers.add(layer)

    form = ExtendedAreaSettingsForm(
        data={
            "polygon": json.dumps(module.settings_instance.polygon),
            "layers": [],
        },
        instance=module,
    )

    assert form.is_valid(), form.errors
    form.save()

    assert module.map_layer_selection.layers.count() == 0


@pytest.mark.django_db
def test_map_layers_only_for_spatial_brainstorming(
    module_factory, area_settings_factory
):
    module = module_factory(blueprint_type="BS")
    area_settings_factory(module=module)

    form = ExtendedAreaSettingsForm(instance=module)

    assert "layers" not in form.fields
    assert get_map_layers(module) == []


@pytest.mark.django_db
def test_area_settings_widget_contains_layer_configuration(
    module_factory, area_settings_factory
):
    module = module_factory(blueprint_type="MBS")
    area_settings_factory(module=module)
    layer = create_layer()

    form = ExtendedAreaSettingsForm(instance=module)
    assert layer.as_dict() in form.fields["polygon"].widget.layers

    output = form.fields["polygon"].widget.render("polygon", None)

    assert "data-map-layers=" in output
    assert "Test layer" in output


@pytest.mark.django_db
def test_map_layer_selection_is_provided_to_frontend(
    module_factory, area_settings_factory
):
    module = module_factory(blueprint_type="MBS")
    area_settings_factory(module=module)
    layer = create_layer()
    selection = ModuleMapLayer.objects.create(module=module)
    selection.layers.add(layer)

    assert get_map_layers(module) == [layer.as_dict()]

    props = get_rendered_props(
        {"module": module},
        "{% load react_mapideas %}{% react_mapideas module %}",
    )

    assert props["map"]["layers"] == [layer.as_dict()]
