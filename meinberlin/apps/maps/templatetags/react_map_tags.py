from django import template

from adhocracy4.maps_react.utils import react_tag_factory


register = template.Library()

register.simple_tag(
    react_tag_factory('display-point'),
    name='react_display_point',
)


