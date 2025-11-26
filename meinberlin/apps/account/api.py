from django.utils import timezone
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.projects.models import Project
from meinberlin.apps.projects import serializers as project_serializers


class EndSessionView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        request.session.flush()
        return Response(status=status.HTTP_200_OK)


class FollowedProjectsListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [ViewSetRulesPermission]

    def get_permission_object(self):
        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.now = timezone.now()

    def get_queryset(self):
        user = self.request.user
        return (
            Project.objects.filter(follow__creator=user, follow__enabled=True)
            .prefetch_related("topics")
            .distinct()
            .order_by("-created")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        projects_list = list(queryset)

        def parse_time_left(time_left_str):
            """Convert 'X days' format to total seconds for comparison"""
            if not time_left_str or time_left_str == "None":
                return float("inf")

            try:
                if "days" in time_left_str:
                    days = float(time_left_str.split(" ")[0])
                    return days * 86400  # Convert to seconds
                return float("inf")
            except (ValueError, IndexError):
                return float("inf")

        def get_sort_key(project):
            # Active projects with time left come first, sorted by shortest time
            if (
                project.module_running_time_left
                and project.module_running_time_left != "None"
            ):
                time_seconds = parse_time_left(project.module_running_time_left)
                return (0, time_seconds)

            # Completed projects - most recent first
            elif project.has_finished and project.end_date:
                return (1, -project.end_date.timestamp())

            # Other projects
            else:
                return (2, 0)

        projects_list.sort(key=get_sort_key)

        serializer = self.get_serializer(projects_list, many=True)
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        if "status" in self.request.GET:
            statustype = self.request.GET["status"]
            if statustype == "activeParticipation":
                return project_serializers.ActiveProjectSerializer(
                    now=self.now, *args, **kwargs
                )
        return project_serializers.ProjectSerializer(now=self.now, *args, **kwargs)
