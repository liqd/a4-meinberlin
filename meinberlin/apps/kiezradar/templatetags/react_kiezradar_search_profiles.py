import json

from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag()
def react_kiezradar_search_profiles():
    attributes = {}

    return format_html(
        '<div data-mb-widget="kiezradar-search-profiles" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
