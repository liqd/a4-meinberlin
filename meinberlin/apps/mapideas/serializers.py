from rest_framework import serializers

from meinberlin.apps.ideas.serializers import IdeaSerializer
from meinberlin.apps.mapideas.models import MapIdea


class MapIdeaSerializer(IdeaSerializer):
    point = serializers.SerializerMethodField()

    class Meta(IdeaSerializer.Meta):
        model = MapIdea
        fields = IdeaSerializer.Meta.fields + ("point",)
        read_only_fields = IdeaSerializer.Meta.read_only_fields + ("point",)

    def get_point(self, instance):
        return instance.point
