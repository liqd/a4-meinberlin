from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import SearchProfile
from .serializers import SearchProfileSerializer


class SearchProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing SearchProfile objects.
    """

    queryset = SearchProfile.objects.select_related("query").all()
    serializer_class = SearchProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override to save the user from the request.
        """
        serializer.save(user=self.request.user)
