from django.core.cache import cache
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.projects.enums import Access
from meinberlin.apps.projectcontainers.models import ProjectContainer
from meinberlin.apps.projectcontainers.serializers import ProjectContainerSerializer


class ProjectContainerViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return ProjectContainer.objects.filter(
            is_draft=False, access=Access.PUBLIC, is_archived=False
        )

    def list(self, request, *args, **kwargs):
        data = cache.get("containers")
        if data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set("containers", data, 300)
        return Response(data)

    def get_serializer(self, *args, **kwargs):
        now = timezone.now()
        return ProjectContainerSerializer(now=now, *args, **kwargs)
