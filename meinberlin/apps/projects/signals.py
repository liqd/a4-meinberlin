from django.core.cache import cache
from django.dispatch import receiver

from adhocracy4.dashboard import signals as a4dashboard_signals


@receiver(a4dashboard_signals.project_created)
def log_project_created(sender, project, user, **kwargs):
    cache.delete("projects_active")
    cache.delete("projects_future")
    cache.delete("projects_past")
    cache.delete("private_projects")


@receiver(a4dashboard_signals.project_published)
def log_project_published(sender, project, user, **kwargs):
    cache.delete("projects_active")
    cache.delete("projects_future")
    cache.delete("projects_past")
    cache.delete("private_projects")


@receiver(a4dashboard_signals.project_unpublished)
def log_project_unpublished(sender, project, user, **kwargs):
    cache.delete("projects_active")
    cache.delete("projects_future")
    cache.delete("projects_past")
    cache.delete("private_projects")
