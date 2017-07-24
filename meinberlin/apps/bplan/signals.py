from django.db.models.signals import post_save
from django.dispatch import receiver

from . import emails
from .models import Statement


@receiver(post_save, sender=Statement)
def send_notification(sender, instance, created, **kwargs):
    if created:
        emails.OfficeWorkerNotification.send(instance)

        if instance.email:
            emails.SubmitterConfirmation.send(instance)
