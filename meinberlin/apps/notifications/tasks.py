from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from meinberlin.apps.notifications.models import Notification


@shared_task(name="periodic_notifications_cleanup")
def periodic_notifications_cleanup():
    """
    This task makes sure that any notification data older >6 months is deleted.
    """
    Notification.objects.filter(
        action__timestamp__gt=timezone.now() - timedelta(days=180)
    ).delete()
