from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save
from django.dispatch import receiver

from adhocracy4.notifications.models import NotificationSettings

from . import emails
from .models import User


@receiver(email_confirmed)
def send_welcome_email(request, email_address, **kwargs):
    user = email_address.user
    emails.WelcomeEmail.send(user)


@receiver(post_save, sender=User)
def create_notification_settings(sender, instance, created, *args, **kwargs):
    """Create notification settings for user"""
    if created and not hasattr(instance, "notification_settings"):
        NotificationSettings.objects.create(user=instance)
