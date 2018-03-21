from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.models.base import UserGeneratedContentModel


class OfflineEvent(UserGeneratedContentModel):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=120, verbose_name=_('Title'))
    date = models.DateTimeField(verbose_name=_('Date'))
    description = RichTextUploadingField(
        config_name='image-editor', verbose_name=_('Description'))
    project = models.ForeignKey(
        'a4projects.Project', on_delete=models.CASCADE, related_name='+')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description = transforms.clean_html_field(
            self.description, 'image-editor')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('meinberlin_offlineevents:offlineevent-detail',
                       args=[str(self.slug)])
