from rest_framework import viewsets

from meinberlin.apps.contrib import caching
from meinberlin.apps.plans.models import Plan
from meinberlin.apps.plans.serializers import PlanSerializer


class PlansViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlanSerializer

    def get_queryset(self):
        return Plan.objects.filter(is_draft=False).prefetch_related("projects")

    def list(self, request, *args, **kwargs):
        context = {"path": request.path}
        return caching.add_or_serialize(
            namespace="plans", view_set=self, context=context
        )
