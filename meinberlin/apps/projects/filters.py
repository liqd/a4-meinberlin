from django.db.models import Q
from rest_framework import filters

from adhocracy4.modules.models import Module


class StatusFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        now = view.now

        if "status" in request.GET:
            status = request.GET["status"]

            has_past_module = Q(module__phase__end_date__lt=now)
            has_active_module = Q(
                module__phase__start_date__lte=now, module__phase__end_date__gt=now
            )
            active_modules = Module.objects.filter(
                phase__start_date__lte=now, phase__end_date__gt=now
            )
            has_future_module = Q(module__phase__start_date__gt=now)

            if status == "activeParticipation":
                return queryset.filter(has_active_module).distinct()

            elif status == "futureParticipation":
                return (
                    queryset.exclude(module__in=active_modules)
                    .filter(has_future_module)
                    .distinct()
                )

            elif status == "pastParticipation":
                return (
                    queryset.exclude(module__in=active_modules)
                    .exclude(has_future_module)
                    .filter(has_past_module)
                    .distinct()
                )

        return queryset
