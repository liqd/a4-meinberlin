import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag()
def react_kiezradar():
    attributes = {
        "apiUrl": reverse("kiezradar-list"),
        "planListUrl": reverse("meinberlin_plans:plan-list"),
        "kiezradarFiltersUrl": reverse("kiezradar_filters"),
        "kiezradarNewUrl": reverse("kiezradar_new"),
    }

    return format_html(
        '<div data-mb-widget="kiezradar" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
