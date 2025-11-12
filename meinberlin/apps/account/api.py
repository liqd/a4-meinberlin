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
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        if "status" in self.request.GET:
            statustype = self.request.GET["status"]
            if statustype == "activeParticipation":
                return project_serializers.ActiveProjectSerializer(
                    now=self.now, *args, **kwargs
                )
        return project_serializers.ProjectSerializer(now=self.now, *args, **kwargs)
