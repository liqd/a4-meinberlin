from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.projects"
    label = "meinberlin_projects"

    def ready(self):
        import meinberlin.apps.projects.signals  # noqa:F401

        from . import overwrites

        overwrites.overwrite_access_enum_label()
