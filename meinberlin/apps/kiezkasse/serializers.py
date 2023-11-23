from ..ideas.serializers import IdeaSerializer
from .models import Proposal


class ProposalSerializer(IdeaSerializer):
    class Meta(IdeaSerializer.Meta):
        model = Proposal
