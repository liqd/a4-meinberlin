from django import template

from meinberlin.apps.cms import models as cms_models
from meinberlin.apps.notifications.models import Notification

register = template.Library()


@register.simple_tag
def get_header_menu(title):
    menu = cms_models.HeaderNavigationMenu.objects.filter(title=title).first()

    if menu is not None:
        return menu.items.all()


@register.simple_tag(takes_context=True)
def get_notifications_count(context):
    request = context.get("request")
    if not request or not request.user.is_authenticated:
        return 0

    unread_count = (
        Notification.objects.filter(recipient=request.user, read=False)
        .exclude(action__actor=request.user)
        .count()
    )

    return unread_count


@register.simple_tag
def get_footer_menu(title):
    menu = cms_models.FooterNavigationMenu.objects.filter(title=title).first()

    if menu is not None:
        return menu.items.all()
