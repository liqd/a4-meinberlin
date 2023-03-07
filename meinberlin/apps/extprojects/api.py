from django.core.cache import cache
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.projects.enums import Access
from meinberlin.apps.extprojects.models import ExternalProject
from meinberlin.apps.extprojects.serializers import ExternalProjectSerializer


class ExternalProjectViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return ExternalProject.objects.filter(
            project_type="meinberlin_extprojects.ExternalProject",
            is_draft=False,
            access=Access.PUBLIC,
            is_archived=False,
        )

    def get_serializer(self, *args, **kwargs):
        now = timezone.now()
        return ExternalProjectSerializer(now=now, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        data = cache.get("ext_projects")
        if data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            cache.set("ext_projects", serializer.data, 300)
            data = serializer.data

        return Response(data)
