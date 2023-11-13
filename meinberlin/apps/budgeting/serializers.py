from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from meinberlin.apps.votes.models import TokenVote
from meinberlin.apps.votes.models import VotingToken

from ..ideas.serializers import IdeaSerializer
from .models import Proposal


class ProposalSerializer(IdeaSerializer):
    session_token_voted = serializers.SerializerMethodField()
    vote_allowed = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()

    class Meta(IdeaSerializer.Meta):
        model = Proposal
        fields = IdeaSerializer.Meta.fields + (
            "is_archived",
            "session_token_voted",
            "vote_allowed",
            "vote_count",
        )
        read_only_fields = IdeaSerializer.Meta.read_only_fields + (
            "is_archived",
            "session_token_voted",
            "vote_allowed",
            "vote_count",
        )

    def get_session_token_voted(self, proposal: Proposal) -> bool:
        """Serialize if proposal has been voted.

        Returns bool that indicates whether the proposal has
        been voted with the token in the current session
        """
        if "request" in self.context:
            if "voting_tokens" in self.context["request"].session:
                module = self.context["view"].module
                module_key = str(module.id)
                if module_key in self.context["request"].session["voting_tokens"]:
                    token = VotingToken.get_voting_token_by_hash(
                        token_hash=self.context["request"].session["voting_tokens"][
                            module_key
                        ],
                        module=module,
                    )
                    if not token:
                        return False
                    vote = TokenVote.objects.filter(
                        token=token,
                        content_type=ContentType.objects.get_for_model(
                            proposal.__class__
                        ),
                        object_pk=proposal.pk,
                    )
                    return vote.exists()
        return False

    def get_vote_allowed(self, proposal: Proposal) -> bool:
        if "request" in self.context:
            user = self.context["request"].user
            has_voting_permission = user.has_perm(
                "meinberlin_budgeting.vote_proposal", proposal
            )
            is_three_phase_budgeting = proposal.module.blueprint_type == "PB3"
            return has_voting_permission and is_three_phase_budgeting

        return False

    def get_vote_count(self, proposal: Proposal) -> int:
        if hasattr(proposal, "token_vote_count"):
            return proposal.token_vote_count
        else:
            return 0
