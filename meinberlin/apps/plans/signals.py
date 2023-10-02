from django.db.models.signals import post_save
from django.dispatch import receiver

from meinberlin.apps.contrib import caching

from .models import Plan


@receiver(post_save, sender=Plan)
def reset_cache(sender, instance, update_fields, **kwargs):
    context = {"trigger": "signal", "plan_id": instance.id}
    caching.delete(namespace="plans", context=context)
