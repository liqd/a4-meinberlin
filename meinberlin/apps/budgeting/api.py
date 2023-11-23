from typing import List

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.filters import SearchFilter

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.modules.predicates import module_is_between_phases
from adhocracy4.phases.predicates import has_feature_active
from meinberlin.apps.contrib.filters import NoExceptionFilterBackend
from meinberlin.apps.contrib.filters import OrderingFilterWithDailyRandom
from meinberlin.apps.ideas.api import BaseIdeaViewSet
from meinberlin.apps.ideas.api import IdeaFilterInfoMixin
from meinberlin.apps.ideas.api import PermissionInfoMixin
from meinberlin.apps.votes.filters import OwnVotesFilterBackend

from ..votes.api import VotingTokenInfoMixin
from .filters import ProposalFilterSet
from .models import Proposal
from .serializers import ProposalSerializer


class ProposalFilterInfoMixin(IdeaFilterInfoMixin):
    def list(self, request, *args, **kwargs):
        """Add the filter information to the data of the Proposal API.

        Needs to be used with rest_framework.mixins.ListModelMixin
        and adhocracy4.api.mixins.ModuleMixin or some other mixin that
        fetches the module
        """
        response = super().list(request, args, kwargs)
        filters = {}

        # archived filter
        filters["is_archived"] = {
            "label": _("Archived"),
            "choices": [
                ("", _("All")),
                ("false", _("No")),
                ("true", _("Yes")),
            ],
            "default": "false",
        }

        # own votes filter
        # only show during voting phase and when token is entered
        if (
            has_feature_active(self.module, Proposal, "vote")
            and "voting_tokens" in request.session
            and str(self.module.id) in request.session["voting_tokens"]
        ):
            filters["own_votes"] = {
                "label": _("Voting"),
                "choices": [
                    ("", _("All")),
                    ("true", _("My votes")),
                ],
            }

        # ordering filter
        ordering_choices = self.get_ordering_choices(request)
        default_ordering = self.get_default_ordering()
        filters["ordering"] = {
            "label": _("Ordering"),
            "choices": ordering_choices,
            "default": default_ordering,
        }

        response.data["filters"].update(filters)
        return response

    def get_ordering_choices(self, request):
        ordering_choices = [
            ("-created", _("Most recent")),
        ]
        # only show sort by rating when rating is allowed at anytime in module
        # like "view_rate_count" from PermissionInfoMixin
        if self.module.has_feature("rate", Proposal):
            ordering_choices += (("-positive_rating_count", _("Most popular")),)
        # only show sort by support option during support phase and btw support
        # and voting phase like "view_support_count" from PermissionInfoMixin
        show_support_option = request.user.has_perm(
            "meinberlin_budgeting.view_support", self.module
        )
        if show_support_option:
            ordering_choices += (("-positive_rating_count", _("Most support")),)

        ordering_choices += (
            ("-comment_count", _("Most commented")),
            ("dailyrandom", _("Random")),
        )

        show_most_votes_option = request.user.has_perm(
            "meinberlin_budgeting.view_vote_count", self.module
        )
        if show_most_votes_option:
            ordering_choices += (("-token_vote_count", _("Most votes")),)

        return ordering_choices

    def get_default_ordering(self):
        """Return current default of ordering filter.

        Between support and voting phase, 'most support' is default ordering
        filter, else dailyrandom
        """
        if module_is_between_phases(
            "meinberlin_budgeting:support", "meinberlin_budgeting:voting", self.module
        ):
            return "-positive_rating_count"
        elif (
            self.module.has_feature("vote", Proposal)
            and self.module.module_has_finished
        ):
            return "-token_vote_count"
        return "dailyrandom"


class ProposalPermissionInfoMixin(PermissionInfoMixin):
    def list(self, request, *args, **kwargs):
        """Add the permission information to the data of the Proposal API.

        Needs to be used with rest_framework.mixins.ListModelMixin
        and adhocracy4.api.mixins.ModuleMixin or some other mixin that
        fetches the module
        """
        response = super().list(request, args, kwargs)
        permissions = {}
        user = request.user
        permissions["view_support_count"] = user.has_perm(
            "meinberlin_budgeting.view_support", self.module
        )
        permissions["view_vote_count"] = user.has_perm(
            "meinberlin_budgeting.view_vote_count", self.module
        )
        permissions[
            "has_voting_permission_and_valid_token"
        ] = self._has_valid_token_in_session(response) and user.has_perm(
            "meinberlin_budgeting.add_vote", self.module
        )

        response.data["permissions"].update(permissions)
        return response

    def _has_valid_token_in_session(self, response):
        if "token_info" in response.data and response.data["token_info"]:
            return True
        return False


class ProposalViewSet(
    ModuleMixin,
    ProposalFilterInfoMixin,
    ProposalPermissionInfoMixin,
    VotingTokenInfoMixin,
    BaseIdeaViewSet,
):
    model = Proposal
    serializer_class = ProposalSerializer
    filter_backends = (
        NoExceptionFilterBackend,
        OrderingFilterWithDailyRandom,
        SearchFilter,
        OwnVotesFilterBackend,
    )
    filterset_class = ProposalFilterSet

    ordering_fields = (
        "created",
        "comment_count",
        "positive_rating_count",
        "dailyrandom",
        "token_vote_count",
    )
    search_fields = ("name", "ref_number")

    @property
    def ordering(self) -> List[str]:
        if module_is_between_phases(
            "meinberlin_budgeting:support", "meinberlin_budgeting:voting", self.module
        ):
            return ["-positive_rating_count"]
        elif (
            self.module.has_feature("vote", Proposal)
            and self.module.module_has_finished
        ):
            return "-token_vote_count"
        return ["dailyrandom"]

    def get_queryset(self) -> QuerySet:
        proposals = super().get_queryset().annotate_token_vote_count()
        return proposals
