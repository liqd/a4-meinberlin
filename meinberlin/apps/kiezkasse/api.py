from typing import List

from django.db.models import QuerySet
from rest_framework.filters import SearchFilter

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.modules.models import Module
from meinberlin.apps.contrib.filters import NoExceptionFilterBackend
from meinberlin.apps.contrib.filters import OrderingFilterWithDailyRandom
from meinberlin.apps.ideas.api import BaseIdeaViewSet
from meinberlin.apps.ideas.api import IdeaFilterInfoMixin
from meinberlin.apps.ideas.api import PermissionInfoMixin
from meinberlin.apps.ideas.filters import IdeaFilterSet
from meinberlin.apps.kiezkasse.models import Proposal
from meinberlin.apps.kiezkasse.serializers import ProposalSerializer


class KiezkasseViewSet(
    ModuleMixin,
    IdeaFilterInfoMixin,
    PermissionInfoMixin,
    BaseIdeaViewSet,
):
    model = Proposal
    serializer_class = ProposalSerializer
    filter_backends = (
        NoExceptionFilterBackend,
        OrderingFilterWithDailyRandom,
        SearchFilter,
    )
    filterset_class = IdeaFilterSet

    ordering_fields = (
        "created",
        "comment_count",
        "positive_rating_count",
        "dailyrandom",
    )
    search_fields = ("name", "ref_number")

    @property
    def ordering(self) -> List[str]:
        return ["dailyrandom"]

    def get_permission_object(self) -> Module:
        return self.module

    def get_queryset(self) -> QuerySet:
        proposals = (
            self.model.objects.filter(module=self.module)
            .annotate_comment_count()
            .annotate_positive_rating_count()
            .annotate_negative_rating_count()
            .annotate_reference_number()
            .order_by("-created")
        )
        return proposals
