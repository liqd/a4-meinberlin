from django.contrib import admin
from django.contrib import auth
from django.http import StreamingHttpResponse
from django.utils.translation import ugettext_lazy as _

from . import models


def export_emails(modeladmin, request, queryset):
    def get_response():
        for obj in queryset:
            yield '{}\n'.format(obj.email)

    response = StreamingHttpResponse(get_response(), content_type='text/csv')
    response[
        'Content-Disposition'] = 'attachment; filename=meinberlin_emails.csv'
    return response


export_emails.short_description = 'Export emails of selected users'


class UserAdmin(auth.admin.UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('username', 'email', 'password1', 'password2'),
    }), )
    readonly_fields = ('date_joined', 'last_login')
    list_display = ('id', 'username', 'email', 'date_joined', 'last_login',
                    'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'last_login')
    search_fields = ('username', 'email', 'id')
    actions = (export_emails, )


admin.site.register(models.User, UserAdmin)
