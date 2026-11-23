import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

from meinberlin.apps.maps.utils import get_map_settings_with_layer

register = template.Library()


@register.simple_tag()
def react_map_topics(module):
    maptopics_api_url = reverse("map-topics-list", kwargs={"module_pk": module.pk})

    attributes = {
        "apiUrl": maptopics_api_url,
        "map": get_map_settings_with_layer(
            module,
            polygon=module.settings_instance.polygon,
        ),
    }

    return format_html(
        '<div data-mb-widget="map-topics" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
