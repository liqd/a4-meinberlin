from django.db import models

from adhocracy4.notifications import models as a4models


class NotificationManager(a4models.NotificationManager):
    pass


class Notification(a4models.Notification):
    search_profile = models.ForeignKey(
        "meinberlin_kiezradar.SearchProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )


class NotificationSettings(a4models.NotificationSettings):
    pass
