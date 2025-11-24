from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.models.base import TimeStampedModel
from adhocracy4.modules import models as module_models
from adhocracy4.projects.models import Topic
from meinberlin.apps.extprojects.models import ExternalProject


class Bplan(ExternalProject):
    is_diplan = models.BooleanField(default=False)
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


class AnonymousItem(TimeStampedModel):
    # TODO: remove this class once transition to diplan is complete
    module = models.ForeignKey(module_models.Module, on_delete=models.CASCADE)

    @property
    def project(self):
        return self.module.project

    @property
    def creator(self):
        return AnonymousUser()

    @creator.setter
    def creator(self, value):
        pass

    class Meta:
        abstract = True


class Statement(AnonymousItem):
    # TODO: remove this class once transition to diplan is complete
    name = models.CharField(max_length=255, verbose_name=_("Your Name"))
    email = models.EmailField(blank=True, verbose_name=_("Email address"))
    statement = models.TextField(verbose_name=_("Statement"))

    street_number = models.CharField(
        max_length=255, verbose_name=_("Street, House number")
    )
    postal_code_city = models.CharField(
        max_length=255, verbose_name=_("Postal code, City")
    )

    class Meta:
        ordering = ["-created"]
