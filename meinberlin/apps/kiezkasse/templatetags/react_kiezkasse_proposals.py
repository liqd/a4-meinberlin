from django import template

from adhocracy4.maps_react.utils import react_tag_factory


register = template.Library()

register.simple_tag(
    react_tag_factory('kiezkasse-proposals', 'kiezkasse-proposals-list'),
    name='react_kiezkasse_proposals',
)
