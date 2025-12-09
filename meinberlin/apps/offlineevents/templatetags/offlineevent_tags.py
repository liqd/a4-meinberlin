from django import template

from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from meinberlin.apps.activities.models import Activity

register = template.Library()


@register.filter
def is_phase(obj):
    return isinstance(obj, Phase)


@register.filter
def is_module(obj):
    return isinstance(obj, Module)


@register.filter
def has_activity(obj):
    try:
        return isinstance(obj.item_set.first().activity, Activity)
    except AttributeError:
        try:
            return isinstance(
                obj.future_phases.first().module.item_set.first().activity, Activity
            )
        except AttributeError:
            return isinstance(obj, Activity)
