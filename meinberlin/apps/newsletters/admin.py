from django.contrib import admin

from adhocracy4.projects.admin import ProjectAdminFilter

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

