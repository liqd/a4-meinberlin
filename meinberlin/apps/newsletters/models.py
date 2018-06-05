import re

from background_task.models import Task
from background_task.models_completed import CompletedTask
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects.models import Project

PLATFORM = 0
ORGANISATION = 1
PROJECT = 2
INITIATOR = 3

RECEIVER_CHOICES = (
    (PROJECT, _('Users following a specific project')),
    (ORGANISATION, _('Users following your organisation')),
    (INITIATOR, _('Every initiator of your organisation')),
    (PLATFORM, _('Every user of the platform'))

)


class Newsletter(UserGeneratedContentModel):

    sender_name = models.CharField(max_length=254,
                                   verbose_name=_('Name'))
    sender = models.EmailField(blank=True,
                               verbose_name=_('Sender'))
    subject = models.CharField(max_length=254,
                               verbose_name=_('Subject'))
    body = RichTextUploadingField(blank=True,
                                  config_name='image-editor',
                                  verbose_name=_('Email body'))
    sent = models.DateTimeField(blank=True,
                                null=True,
                                verbose_name=_('Sent'))

    receivers = models.PositiveSmallIntegerField(choices=RECEIVER_CHOICES,
                                                 verbose_name=_('Receivers'))

    project = models.ForeignKey(Project,
                                null=True, blank=True,
                                on_delete=models.CASCADE)

    organisation = models.ForeignKey(settings.A4_ORGANISATIONS_MODEL,
                                     null=True, blank=True,
                                     on_delete=models.CASCADE)

    completed_tasks = GenericRelation(CompletedTask,
                                      content_type_field='creator_content_type', # noqa
                                      object_id_field='creator_object_id')
    tasks = GenericRelation(Task,
                            content_type_field='creator_content_type',
                            object_id_field='creator_object_id')

    @cached_property
    def body_with_absolute_urls(self):
        return self.replace_relative_media_urls(self.body)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        # Delete cached properties
        try:
            if key == 'body':
                del self.body_with_absolute_urls
        except AttributeError:
            pass

    @staticmethod
    def replace_relative_media_urls(text):
        if not settings.MEDIA_URL.startswith('/'):
            # Replace only if MEDIA_URL is relative
            return text

        # Find every occurrence of the MEDIA_URL that is either following a
        # whitespace, an equal sign or a quotation mark.
        pattern = re.compile(r'([\s="\'])(%s)' % re.escape(settings.MEDIA_URL))
        text = re.sub(pattern, r'\1%s\2' % settings.BASE_URL, text)
        return text

    def save(self, *args, **kwargs):
        self.body = transforms.clean_html_field(self.body, 'image-editor')
        super().save(*args, **kwargs)
