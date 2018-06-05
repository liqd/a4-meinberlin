import json

from django.contrib import admin

from adhocracy4.projects.admin import ProjectAdminFilter
from adhocracy4.emails.tasks import deserialize_email
from background_task.models_completed import CompletedTask
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from . import models


@admin.register(models.Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent', 'project', 'email_status')
    list_filter = (
        'project__organisation',
        'project__is_archived',
        ProjectAdminFilter
    )
    date_hierarchy = 'sent'
    readonly_fields = ['email_status']
    
    def email_status(self, newsletter):
        queue = newsletter.tasks.count()
        success = newsletter.completed_tasks.filter(last_error='').count()
        errors = newsletter.completed_tasks.exclude(last_error='').count()
        return '<a href="{url}?creator_object_id={newsletter_id}">{errors} errors; {success} success</a>; {queue} in queue'.format(
            queue=queue,
            success=success,
            errors=errors,
            url=reverse('admin:meinberlin_newsletters_newslettertask_changelist'),
            newsletter_id=newsletter.id)
    email_status.allow_tags = True

# Kind of a hack so we can have tasks two times in the admin interface
class NewsletterTask(CompletedTask):
    class Meta:
        proxy = True
        verbose_name = 'Newsletter send Email'

@admin.register(NewsletterTask)
class NewsletterTaskAdmin(admin.ModelAdmin):
    
    list_display = ['verbose_name', 'newsletter_id', 'last_error_line']
    list_filter = ['creator_object_id']
    readonly_fields = ['raw_email']

    def get_queryset(self, request):
        newsletter_content_type = ContentType.objects.get(app_label='meinberlin_newsletters', model='newsletter')
        qs = super().get_queryset(request).filter(creator_content_type=newsletter_content_type.pk)
        return qs

    def newsletter_id(self, task):
        url = reverse('admin:meinberlin_newsletters_newsletter_change', args=[task.creator.id])
        return '<a href="{}">{}</a>'.format(url, task.creator.id)  # no escaping
    newsletter_id.allow_tags = True
    newsletter_id.admin_order_field = 'creator_object_id'

    def last_error_line(self, task):
        lines = task.last_error.splitlines()
        if lines:
            return lines[-1]
    last_error_line.admin_order_field = 'last_error'

    def raw_email(self, task):
        task_args, task_kwargs = json.loads(task.task_params)
        email = deserialize_email(task_args[0])
        return  email.message()
