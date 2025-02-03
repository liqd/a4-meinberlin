from django import template

register = template.Library()


@register.simple_tag
def modify_hero_content(content):
    """Creates a modified copy of the content object with point_label as description"""
    # Create a copy of the object to avoid modifying the original
    from copy import copy

    modified_content = copy(content)
    # Override the description with point_label
    modified_content.description = content.point_label
    # Replace title with the name field dynamically
    modified_content.name = modified_content.title

    return modified_content
