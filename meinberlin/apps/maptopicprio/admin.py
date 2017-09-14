from django.contrib import admin

from adhocracy4.modules import admin as module_admin

from . import models

admin.site.register(models.MapTopic, module_admin.ItemAdmin)
