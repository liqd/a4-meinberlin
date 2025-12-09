from django.db import transaction
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        user = request.user

        with transaction.atomic():
            from django.contrib.auth import get_user_model

            User = get_user_model()

            locked_user = User.objects.select_for_update().get(id=user.id)

            current_count = KiezRadar.objects.filter(creator=locked_user).count()

            if current_count >= KiezRadar.KIEZRADAR_LIMIT:
                raise ValidationError(
                    detail={
                        "error": f"Users can only have up to {KiezRadar.KIEZRADAR_LIMIT} kiezradar filters."
                    }
                )

            # Create serializer WITHOUT the validation check (or with safe version)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            instance = serializer.save(creator=locked_user)

            response_serializer = self.get_serializer(instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

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
