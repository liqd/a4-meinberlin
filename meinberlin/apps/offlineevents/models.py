from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.modules import models as module_models

# Offline Event Modul Area


class OfflineEventItem(module_models.Item):
    name = models.CharField(
        max_length=120, verbose_name=_("Name"), null=True, blank=True
    )
    event_date = models.DateTimeField(verbose_name=_("Date"), null=True, blank=True)
    event_type = models.CharField(
        max_length=30, verbose_name=_("Event type"), null=True, blank=True
    )
    description = CKEditor5Field(
        config_name="collapsible-image-editor",
        verbose_name=_("Description"),
        validators=[ImageAltTextValidator()],
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.event_date or not self.module_id:
            return
        phase = self.module.phase_set.order_by("weight").first()
        phase.start_date = self.event_date
        phase.end_date = self.event_date
        phase.save(update_fields=["start_date", "end_date"])

        if self.name:
            self.module.name = self.name
            self.module.save()
