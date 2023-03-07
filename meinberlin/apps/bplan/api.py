from django.core.cache import cache
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response

from adhocracy4.api.mixins import OrganisationMixin
from adhocracy4.api.permissions import ViewSetRulesPermission

from .models import Bplan
from .serializers import BplanSerializer


class BplanViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    OrganisationMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BplanSerializer
    permission_classes = (ViewSetRulesPermission,)

    def get_permission_object(self):
        return self.organisation

    def get_queryset(self):
        return Bplan.objects.filter(organisation=self.organisation)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "organisation_pk": self.organisation_pk,
            }
        )
        return context

    def list(self, request, *args, **kwargs):
        data = cache.get("bplans_" + self.organisation.slug)
        if data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            cache.set("bplans_" + self.organisation.slug, data, 300)
            data = serializer.data

        return Response(data)
