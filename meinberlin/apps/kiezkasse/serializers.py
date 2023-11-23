from meinberlin.apps.ideas.serializers import IdeaSerializer
from meinberlin.apps.kiezkasse.models import Proposal


class ProposalSerializer(IdeaSerializer):
    class Meta(IdeaSerializer.Meta):
        model = Proposal
