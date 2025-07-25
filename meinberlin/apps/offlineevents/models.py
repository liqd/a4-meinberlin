from datetime import timedelta

from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4 import transforms
from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects import models as project_models


class OfflineEventsQuerySet(models.QuerySet):
    def starts_within(self, hours=72):
        """All offlineevents starting within the given time."""
        now = timezone.now()
        return self.filter(date__gt=now, date__lt=(now + timedelta(hours=hours)))


class OfflineEvent(UserGeneratedContentModel):
    slug = AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=120, verbose_name=_("Name of event"))
    event_type = models.CharField(
        max_length=30,
        verbose_name=_("Event type"),
    )
    date = models.DateTimeField(verbose_name=_("Date"))
    description = CKEditor5Field(
        config_name="collapsible-image-editor",
        verbose_name=_("Description"),
        validators=[ImageAltTextValidator()],
    )
    project = models.ForeignKey(project_models.Project, on_delete=models.CASCADE)

    objects = OfflineEventsQuerySet.as_manager()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.name

    def save(self, update_fields=None, *args, **kwargs):
        self.description = transforms.clean_html_field(
            self.description, "collapsible-image-editor"
        )
        if update_fields:
            update_fields = {"description"}.union(update_fields)
        super().save(update_fields=update_fields, *args, **kwargs)

    @cached_property
    def get_timeline_index(self):
        if self.project.display_timeline:
            for count, cluster in enumerate(self.project.participation_dates):
                if "event_type" in cluster and self.slug == cluster["slug"]:
                    return count
        return 0

    def get_absolute_url(self):
        return reverse(
            "project-event", kwargs={"slug": self.project.slug, "event_slug": self.slug}
        )

    @cached_property
    def is_past(self):
        return self.date < timezone.now()
