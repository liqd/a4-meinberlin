from django.contrib import admin
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _

from . import models


class UserAdmin(auth.admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')
    list_display = (
        'username', 'email', 'date_joined', 'is_staff', 'is_superuser'
    )
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email')


admin.site.register(models.User, UserAdmin)
