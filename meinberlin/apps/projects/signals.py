from django.db.models.signals import post_save
from django.dispatch import receiver

from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.projects.models import Project
from meinberlin.apps.contrib import caching


@receiver(a4dashboard_signals.project_unpublished)
@receiver(a4dashboard_signals.project_published)
@receiver(a4dashboard_signals.project_created)
def post_dashboard_signal_delete(sender, project, user, **kwargs):
    delete_projects_cache(project=project)


@receiver(post_save, sender=Project)
def post_save_delete(sender, instance, update_fields, **kwargs):
    delete_projects_cache(project=instance)


def delete_projects_cache(project: Project):
    context = {"trigger": "signal", "project_id": project.id}
    caching.delete(namespace="projects", context=context)
    caching.delete(namespace="privateprojects", context=context)
