from urllib.parse import urlencode

from django import template
from django.urls import reverse

from ..constants import GUEST_SWITCH_QUERY_PARAM
from .userindicator import get_next_url

register = template.Library()


def _url_with_next(url_name, request):
    return f"{reverse(url_name)}?{urlencode({'next': get_next_url(request)})}"


@register.simple_tag(takes_context=True)
def guest_convert_url(context):
    """Return the guest conversion URL, returning to the current page."""
    request = context.get("request")
    if not request:
        return reverse("guest_convert")
    return _url_with_next("guest_convert", request)


@register.simple_tag(takes_context=True)
def guest_personal_login_url(context):
    """Log the guest out before sending them to the personal login page."""
    request = context.get("request")
    if not request:
        return reverse("account_login")
    login_url = _url_with_next("account_login", request)
    query = urlencode({"next": login_url})
    return f"{reverse('account_logout')}?{GUEST_SWITCH_QUERY_PARAM}=1&{query}"
