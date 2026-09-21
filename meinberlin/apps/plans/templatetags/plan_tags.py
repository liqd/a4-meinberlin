from copy import copy

from django import template
from django.template.defaultfilters import linebreaksbr

register = template.Library()


@register.simple_tag
def modify_hero_content(content):
    """Creates a modified copy of the content object with point_label as description"""
    # Create a copy of the object to avoid modifying the original
    modified_content = copy(content)
    # Override the description with point_label, preserving line breaks
    modified_content.description = linebreaksbr(content.point_label or "")
    # Replace title with the name field dynamically
    modified_content.name = modified_content.title

    return modified_content
