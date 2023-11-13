import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def react_ideas(context, module):
    ideas_api_url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    attributes = {
        "ideas_api_url": ideas_api_url,
    }

    return format_html(
        '<div data-mb-widget="ideas" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
