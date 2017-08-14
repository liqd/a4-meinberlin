from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property

from adhocracy4 import transforms
from adhocracy4.comments import models as comment_models
from adhocracy4.models import base
from adhocracy4.modules import models as module_models


class Chapter(module_models.Item):
    name = models.CharField(max_length=120)
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='chapter',
                               object_id_field='object_pk')
    weight = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('weight',)

    def __str__(self):
        return "{}_chapter_{}".format(str(self.module), self.pk)

    def get_absolute_url(self):
        return reverse('meinberlin_documents:chapter-detail',
                       args=[str(self.pk)])

    @cached_property
    def prev(self):
        return Chapter.objects\
            .filter(module=self.module)\
            .filter(weight__lt=self.weight)\
            .order_by('-weight')\
            .first()

    @cached_property
    def next(self):
        return Chapter.objects\
            .filter(module=self.module)\
            .filter(weight__gt=self.weight)\
            .order_by('weight')\
            .first()


class Paragraph(base.TimeStampedModel):
    name = models.CharField(max_length=120, blank=True)
    text = RichTextUploadingField(config_name='image-editor')
    weight = models.PositiveIntegerField()
    chapter = models.ForeignKey(Chapter,
                                on_delete=models.CASCADE,
                                related_name='paragraphs')
    comments = GenericRelation(comment_models.Comment,
                               related_query_name='paragraph',
                               object_id_field='object_pk')

    class Meta:
        ordering = ('weight',)

    def __str__(self):
        return "{}_paragraph_{}".format(str(self.chapter), self.weight)

    def save(self, *args, **kwargs):
        self.text = transforms.clean_html_field(
            self.text, 'image-editor')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('meinberlin_documents:paragraph-detail',
                       args=[str(self.pk)])

    @property
    def creator(self):
        return self.chapter.creator

    @property
    def project(self):
        return self.module.project

    @property
    def module(self):
        return self.chapter.module
