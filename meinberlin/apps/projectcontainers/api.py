from django.utils import timezone
from rest_framework import viewsets

from adhocracy4.projects.enums import Access
from meinberlin.apps.contrib import caching
from meinberlin.apps.projectcontainers.models import ProjectContainer
from meinberlin.apps.projectcontainers.serializers import ProjectContainerSerializer


class ProjectContainerViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return ProjectContainer.objects.filter(
            is_draft=False, access=Access.PUBLIC, is_archived=False
        )

    def get_serializer(self, *args, **kwargs):
        now = timezone.now()
        return ProjectContainerSerializer(now=now, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        context = {"path": request.path}
        return caching.add_or_serialize(
            namespace="projectcontainers", view_set=self, context=context
        )
