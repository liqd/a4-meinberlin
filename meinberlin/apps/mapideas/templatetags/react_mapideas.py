import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

from meinberlin.apps.maps.utils import get_map_settings_with_layer

register = template.Library()


@register.simple_tag()
def react_mapideas(module):
    mapideas_api_url = reverse("mapideas-list", kwargs={"module_pk": module.pk})

    attributes = {
        "apiUrl": mapideas_api_url,
        "map": get_map_settings_with_layer(
            module,
            polygon=module.settings_instance.polygon,
        ),
    }

    return format_html(
        '<div data-mb-widget="map-ideas" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
