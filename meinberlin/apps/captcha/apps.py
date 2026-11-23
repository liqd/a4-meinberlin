from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.captcha"
    label = "meinberlin_captcha"

    def ready(self):
        from . import checks  # noqa: F401
