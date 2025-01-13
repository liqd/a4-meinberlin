from rest_framework import viewsets

from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import KiezRadar
from .models import SearchProfile
from .serializers import KiezRadarSerializer
from .serializers import SearchProfileSerializer


class KiezRadarViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing KiezRadar objects.
    """

    queryset = KiezRadar.objects.all()
    serializer_class = KiezRadarSerializer
    permission_classes = [ViewSetRulesPermission]

    def perform_create(self, serializer):
        """
        Override to save the user from the request.
        """
        serializer.save(creator=self.request.user)

    def get_permission_object(self):
        return None

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return KiezRadar.objects.filter(creator=self.request.user)
        return KiezRadar.objects.none()


class SearchProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing SearchProfile objects.
    """

    queryset = SearchProfile.objects.select_related("query").all()
    serializer_class = SearchProfileSerializer
    permission_classes = [ViewSetRulesPermission]

    def perform_create(self, serializer):
        """
        Override to save the user from the request.
        """
        serializer.save(creator=self.request.user)

    def get_permission_object(self):
        return None

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SearchProfile.objects.filter(creator=self.request.user)
        return SearchProfile.objects.none()
