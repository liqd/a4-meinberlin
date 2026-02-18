from django import template

from meinberlin.apps.offlineevents.models import OfflineEventItem

register = template.Library()


@register.simple_tag
def get_offline_event(phase):
    """
    Get the offline event for a phase's module.
    Usage: {% get_offline_event action.obj as event %}
    """
    if not phase or not hasattr(phase, "module"):
        return None

    # Direct query by module_id
    try:
        return OfflineEventItem.objects.filter(module_id=phase.module.id).first()
    except Exception:
        # Log the error if needed, but return None gracefully
        return None
