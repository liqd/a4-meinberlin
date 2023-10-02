from django.db.models.signals import post_save
from django.dispatch import receiver

from meinberlin.apps.contrib import caching

from .models import ProjectContainer


@receiver(post_save, sender=ProjectContainer)
def reset_cache(sender, instance, update_fields, **kwargs):
    context = {"trigger": "signal", "project_container_id": instance.id}
    caching.delete(namespace="projectcontainers", context=context)
