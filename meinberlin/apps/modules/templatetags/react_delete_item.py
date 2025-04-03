import json

from django import template
from django.urls import reverse
from django.utils.html import format_html

from adhocracy4.modules.models import Item

register = template.Library()


@register.simple_tag(takes_context=False)
def react_delete_item(obj: Item):
    if hasattr(obj, "meinberlin_budgeting_proposal") or hasattr(
        obj, "meinberlin_kiezkasse_proposal"
    ):
        item_type = "proposal"
    else:
        item_type = "idea"

    attributes = {
        "apiUrl": reverse("items-detail", args=[obj.id]),
        "successUrl": reverse("module-detail", args=[obj.module.slug]),
        "itemType": item_type,
    }

    return format_html(
        '<div data-mb-widget="delete-item" ' 'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
