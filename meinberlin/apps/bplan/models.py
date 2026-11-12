from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.projects.models import Topic
from meinberlin.apps.extprojects.models import ExternalProject


class Bplan(ExternalProject):
    office_worker_email = models.EmailField(
        verbose_name=_("Office worker email"),
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Add the topic if it's not already there
        topic = Topic.objects.get(code="URB")
        if not self.topics.filter(code="URB").exists():
            self.topics.add(topic)
