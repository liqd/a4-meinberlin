from django.db.models.signals import post_save
from django.dispatch import receiver

from meinberlin.apps.contrib import caching
from meinberlin.apps.extprojects.models import ExternalProject


@receiver(post_save, sender=ExternalProject)
def reset_cache(sender, instance, update_fields, **kwargs):
    caching.delete(namespace="externalprojects")
