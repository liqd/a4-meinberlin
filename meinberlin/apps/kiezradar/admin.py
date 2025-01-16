from django.contrib import admin

from .models import KiezRadar
from .models import KiezradarQuery
from .models import ProjectType
from .models import SearchProfile


class SearchProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "number")
    readonly_fields = ("number",)
    list_filter = (
        "name",
        "status",
    )


class KiezRadarAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)


class KiezradarQueryAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    list_filter = ("text",)


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "participation")
    list_filter = ("participation",)


admin.site.register(SearchProfile, SearchProfileAdmin)
admin.site.register(KiezRadar, KiezRadarAdmin)
admin.site.register(KiezradarQuery, KiezradarQueryAdmin)
admin.site.register(ProjectType, ProjectTypeAdmin)
