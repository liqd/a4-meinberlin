import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def react_map_topics(context, module):
    map_topics_api_url = reverse("map-topics-list", kwargs={"module_pk": module.pk})

    attributes = {
        "map_topics_api_url": map_topics_api_url,
    }

    return format_html(
        '<div data-mb-widget="map-topics" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
