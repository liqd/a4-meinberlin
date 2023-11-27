import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def react_mapideas(context, module):
    mapideas_api_url = reverse("mapideas-list", kwargs={"module_pk": module.pk})

    attributes = {
        "mapideas_api_url": mapideas_api_url,
    }

    return format_html(
        '<div data-mb-widget="map_ideas" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
