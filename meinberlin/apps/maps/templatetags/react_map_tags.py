import json

from django import template
from django.utils.html import format_html

from adhocracy4.maps_react.utils import get_map_settings

register = template.Library()


@register.simple_tag()
def react_display_point(module, point):

    attributes = {
        "map": get_map_settings(polygon=module.settings_instance.polygon,
                                point=point)
    }

    return format_html(
        '<div data-mb-widget="display-point" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
