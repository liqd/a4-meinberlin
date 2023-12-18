import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def react_topics(context, module):
    topics_api_url = reverse("topics-list", kwargs={"module_pk": module.pk})

    attributes = {
        "apiUrl": topics_api_url,
    }

    return format_html(
        '<div data-mb-widget="topics" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
