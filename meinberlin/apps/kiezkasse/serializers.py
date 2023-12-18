from rest_framework import serializers

from meinberlin.apps.ideas.serializers import IdeaSerializer
from meinberlin.apps.kiezkasse.models import Proposal


class ProposalSerializer(IdeaSerializer):
    point = serializers.SerializerMethodField()

    class Meta(IdeaSerializer.Meta):
        model = Proposal
        fields = IdeaSerializer.Meta.fields + ("point",)

    def get_point(self, instance):
        return instance.point
