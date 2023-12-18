from django import template

from adhocracy4.maps_react.utils import react_tag_factory


register = template.Library()

register.simple_tag(
    react_tag_factory('map-topics', 'map-topics-list'),
    name='react_map_topics',
)
