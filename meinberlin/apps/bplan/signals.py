from django.db.models.signals import post_save
from django.dispatch import receiver

from . import emails
from .models import Bplan
from .models import Statement


@receiver(post_save, sender=Statement)
def send_notification(sender, instance, created, **kwargs):
    if created:
        emails.OfficeWorkerNotification.send(instance)

        if instance.email:
            emails.SubmitterConfirmation.send(instance)


@receiver(post_save, sender=Bplan)
def send_update(sender, instance, update_fields, **kwargs):
    """Sends an email to the responsible person in the administration to notify them
    about changes to the bplan. Should not be triggered when fetching the location or when archived
    """
    # TODO: the if statement can be removed once the transition to diplan is complete
    if not update_fields or (
        "point" not in update_fields and "is_archived" not in update_fields
    ):
        emails.OfficeWorkerUpdateConfirmation.send(instance)
