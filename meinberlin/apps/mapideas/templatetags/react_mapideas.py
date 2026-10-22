import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

from adhocracy4.maps_react.utils import get_map_settings
from meinberlin.apps.maps.models import ModuleMapLayer

register = template.Library()


def get_map_layers(module):
    if module.blueprint_type != "MBS":
        return []
    selection = ModuleMapLayer.objects.filter(module=module).first()
    if not selection:
        return []
    return [layer.as_dict() for layer in selection.layers.all()]


@register.simple_tag()
def react_mapideas(module):
    mapideas_api_url = reverse("mapideas-list", kwargs={"module_pk": module.pk})
    map_settings = get_map_settings(polygon=module.settings_instance.polygon)
    map_settings["layers"] = get_map_layers(module)

    attributes = {"apiUrl": mapideas_api_url, "map": map_settings}

    return format_html(
        '<div data-mb-widget="map-ideas" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
