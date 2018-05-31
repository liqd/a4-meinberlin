from django.contrib import admin

from adhocracy4.projects.admin import ProjectAdminFilter
from background_task.models_completed import CompletedTask
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from . import models


@admin.register(models.Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent', 'project', 'organisation', 'errors')
    list_filter = (
        'project__organisation',
        'project__is_archived',
        ProjectAdminFilter
    )
    date_hierarchy = 'sent'
    
    def errors(self, newsletter):
        return '<a href="/">{}/{}</a>'.format(newsletter.tasks.exclude(last_error='').count(),
                newsletter.tasks.count())
    errors.allow_tags = True

class NewsletterTask(CompletedTask):
    class Meta:
        proxy = True

@admin.register(NewsletterTask)
class NewsletterTaskAdmin(admin.ModelAdmin):
    
    list_display = ['verbose_name', 'newsletter_id', 'newsletter_organisation', 'last_error_line']

    def get_queryset(self, request):
        #assert 0, request
        newsletter_content_type = ContentType.objects.get(app_label='meinberlin_newsletters', model='newsletter')
        qs = super().get_queryset(request).filter(creator_content_type=newsletter_content_type.pk)
        newsletter_id = request.GET.get('filter_by_creator')
        if newsletter_id:
            return qs.filter(creator_object_id=newsletter_id)
        return qs

    def newsletter_id(self, task):
        if task.creator:
            url = reverse('admin:meinberlin_newsletters_newsletter_change', args=[task.creator.id])
            return '<a href="{}">{}</a>'.format(url, task.creator.id)  # no escaping
    newsletter_id.allow_tags = True

    def newsletter_organisation(self, task):
        if task.creator:
            return task.creator.organisation

    def last_error_line(self, task):
        lines = task.last_error.splitlines()
        if lines:
            return lines[-1]
