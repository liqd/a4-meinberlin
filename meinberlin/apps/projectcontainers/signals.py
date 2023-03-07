from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProjectContainer


@receiver(post_save, sender=ProjectContainer)
def reset_cache(sender, instance, update_fields, **kwargs):
    cache.delete("containers")
