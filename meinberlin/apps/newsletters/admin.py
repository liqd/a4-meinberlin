from django.contrib import admin

from adhocracy4.projects.admin import ProjectAdminFilter
from background_task.models_completed import CompletedTask
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from . import models


@admin.register(models.Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent', 'project', 'mail_status')
    list_filter = (
        'project__organisation',
        'project__is_archived',
        ProjectAdminFilter
    )
    date_hierarchy = 'sent'
    
    #def errors(self, newsletter):
        #return '<a href="{}?creator_object_id={}">{}/{}</a>'.format(
                        #reverse('admin:meinberlin_newsletters_newslettertask_changelist'),
                        #newsletter.id,
                        #newsletter.completed_tasks.exclude(last_error='').count(),
                        #newsletter.completed_tasks.count())
    #errors.allow_tags = True

    def mail_status(self, newsletter):
        queue = newsletter.tasks.count()
        success = newsletter.completed_tasks.filter(last_error='').count()
        errors = newsletter.completed_tasks.exclude(last_error='').count()
        return '<a href="{url}?creator_object_id={newsletter_id}">{errors} errors; {success} success</a>; {queue} in queue'.format(
            queue=queue,
            success=success,
            errors=errors,
            url=reverse('admin:meinberlin_newsletters_newslettertask_changelist'),
            newsletter_id=newsletter.id)
    mail_status.allow_tags = True

class NewsletterTask(CompletedTask):
    class Meta:
        proxy = True

@admin.register(NewsletterTask)
class NewsletterTaskAdmin(admin.ModelAdmin):
    
    list_display = ['verbose_name', 'newsletter_id', 'last_error_line']
    list_filter = ['creator_object_id']

    def get_queryset(self, request):
        #import pdb; pdb.set_trace()
        newsletter_content_type = ContentType.objects.get(app_label='meinberlin_newsletters', model='newsletter')
        qs = super().get_queryset(request).filter(creator_content_type=newsletter_content_type.pk)
        newsletter_id = request.GET.get('creator_object_id')
        if newsletter_id:
            return qs.filter(creator_object_id=newsletter_id)
        return qs

    def newsletter_id(self, task):
        if task.creator:
            url = reverse('admin:meinberlin_newsletters_newsletter_change', args=[task.creator.id])
            return '<a href="{}">{}</a>'.format(url, task.creator.id)  # no escaping
    newsletter_id.allow_tags = True
    newsletter_id.admin_order_field = 'creator_object_id'

    def last_error_line(self, task):
        lines = task.last_error.splitlines()
        if lines:
            return lines[-1]
    last_error_line.admin_order_field = 'last_error'
