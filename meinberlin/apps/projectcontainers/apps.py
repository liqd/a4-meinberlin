from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.projectcontainers"
    label = "meinberlin_projectcontainers"

    def ready(self):
        import meinberlin.apps.projectcontainers.signals  # noqa:F401
