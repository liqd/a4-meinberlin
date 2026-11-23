import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

from meinberlin.apps.maps.utils import get_map_settings_with_layer

register = template.Library()


@register.simple_tag()
def react_proposals(module):
    proposals_api_url = reverse("proposals-list", kwargs={"module_pk": module.pk})
    end_session_url = reverse("end_session")

    attributes = {
        "apiUrl": proposals_api_url,
        "endSessionUrl": end_session_url,
        "map": get_map_settings_with_layer(
            module,
            polygon=module.settings_instance.polygon,
        ),
    }

    return format_html(
        '<div data-mb-widget="proposals" data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
