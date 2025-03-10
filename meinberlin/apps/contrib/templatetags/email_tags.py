from typing import Optional

from django.conf import settings
from django.contrib.sites.models import Site
from django.templatetags.static import register


@register.simple_tag
def get_domain() -> Optional[str]:
    site = None
    if hasattr(settings, "SITE_ID"):
        site = Site.objects.get(pk=settings.SITE_ID)

    if site is None:
        return ""

    ssl_enabled = True
    if site.domain.startswith("localhost:"):
        ssl_enabled = False

    url = "http{ssl_flag}://{domain}".format(
        ssl_flag="s" if ssl_enabled else "",
        domain=site.domain,
    )
    return url
