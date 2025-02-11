import json

from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag()
def react_kiezradar():
    attribution = ""
    mapbox_token = ""
    omt_token = ""

    if hasattr(settings, "A4_MAP_ATTRIBUTION"):
        attribution = settings.A4_MAP_ATTRIBUTION

    if hasattr(settings, "A4_MAPBOX_TOKEN"):
        mapbox_token = settings.A4_MAPBOX_TOKEN

    if hasattr(settings, "A4_OPENMAPTILES_TOKEN"):
        omt_token = settings.A4_OPENMAPTILES_TOKEN

    attributes = {
        "apiUrl": reverse("kiezradar-list"),
        "planListUrl": reverse("meinberlin_plans:plan-list"),
        "kiezradarFiltersUrl": reverse("kiezradar_filters"),
        "kiezradarNewUrl": reverse("kiezradar_new"),
        "attribution": attribution,
        "bounds": json.dumps(settings.A4_MAP_BOUNDING_BOX),
        "baseUrl": settings.A4_MAP_BASEURL,
        "mapboxToken": mapbox_token,
        "omtToken": omt_token,
        "polygon": settings.BERLIN_POLYGON,
    }

    return format_html(
        '<div data-mb-widget="kiezradar" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
