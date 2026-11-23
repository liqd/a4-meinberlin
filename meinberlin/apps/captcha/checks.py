from django.conf import settings
from django.core.checks import Error
from django.core.checks import Tags
from django.core.checks import register

from adhocracy4.captcha.verification import get_captcha_type


@register(Tags.security)
def cap_captcha_configuration_check(app_configs, **kwargs):
    if get_captcha_type() != "cap":
        return []

    required = (
        "A4_CAP_CAPTCHA_ENDPOINT",
        "A4_CAP_CAPTCHA_SECRET",
        "A4_CAP_CAPTCHA_WIDGET_URL",
    )
    missing = [name for name in required if not getattr(settings, name, "")]
    if not missing:
        return []

    return [
        Error(
            "Cap captcha is selected but not fully configured.",
            hint="Set " + ", ".join(missing) + " or switch A4_CAPTCHA_TYPE back.",
            id="meinberlin_captcha.E001",
        )
    ]
