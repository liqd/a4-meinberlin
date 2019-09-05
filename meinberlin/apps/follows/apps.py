from django.apps import AppConfig


class Config(AppConfig):
    name = 'meinberlin.apps.follows'
    label = 'meinberlin_follows'

    def ready(self):
        import meinberlin.apps.follows.signals  # noqa:F401
