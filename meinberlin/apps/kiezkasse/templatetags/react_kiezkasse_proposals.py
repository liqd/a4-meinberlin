import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def react_kiezkasse_proposals(context, module):
    kiezkasse_proposals_api_url = reverse(
        "kiezkasse-proposals-list", kwargs={"module_pk": module.pk}
    )

    attributes = {
        "kiezkasse_proposals_api_url": kiezkasse_proposals_api_url,
    }

    return format_html(
        '<div data-mb-widget="kiezkasse-proposals" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
