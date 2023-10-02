from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from adhocracy4.projects.enums import Access
from adhocracy4.projects.models import Project
from meinberlin.apps.contrib import caching
from meinberlin.apps.projects import serializers as project_serializers
from meinberlin.apps.projects.filters import StatusFilter


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, StatusFilter)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.now = now

    def get_queryset(self):
        projects = (
            Project.objects.filter(
                Q(project_type="a4projects.Project")
                | Q(project_type="meinberlin_bplan.Bplan")
            )
            .filter(
                Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
                is_draft=False,
                is_archived=False,
            )
            .order_by("created")
            .select_related("administrative_district", "organisation")
            .prefetch_related(
                "moderators",
                "plans",
                "organisation__initiators",
                "module_set__phase_set",
            )
        )
        return projects

    def list(self, request, *args, **kwargs):
        return caching.add_or_serialize(
            namespace="projects",
            suffix=self.request.GET.get("status"),
            context={"path": request.path},
            view_set=self,
        )

    def get_serializer(self, *args, **kwargs):
        if "status" in self.request.GET:
            status = self.request.GET["status"]
            if status == "activeParticipation":
                return project_serializers.ActiveProjectSerializer(
                    now=self.now, *args, **kwargs
                )
            if status == "futureParticipation":
                return project_serializers.FutureProjectSerializer(
                    now=self.now, *args, **kwargs
                )
            if status == "pastParticipation":
                return project_serializers.PastProjectSerializer(
                    now=self.now, *args, **kwargs
                )
        return project_serializers.ProjectSerializer(now=self.now, *args, **kwargs)


class PrivateProjectViewSet(viewsets.ReadOnlyModelViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.now = now

    def get_queryset(self):
        filter_kwargs = dict(is_draft=False, is_archived=False, access=Access.PRIVATE)
        projects = caching.add_or_query(
            namespace="privateprojects",
            query_set=Project.objects,
            filter_kwargs=filter_kwargs,
        )

        if projects:
            not_accessible = [
                project.id
                for project in projects
                if not self.request.user.has_perm("a4projects.view_project", project)
            ]
            return projects.exclude(id__in=not_accessible)
        else:
            return projects

    def get_serializer(self, *args, **kwargs):
        return project_serializers.ProjectSerializer(now=self.now, *args, **kwargs)
