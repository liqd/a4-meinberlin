from meinberlin.apps.maptopicprio.models import MapTopic
from meinberlin.apps.topicprio.serializers import TopicSerializer


class MapTopicSerializer(TopicSerializer):
    class Meta(TopicSerializer.Meta):
        model = MapTopic
        fields = TopicSerializer.Meta.fields + ("point",)
        read_only_fields = TopicSerializer.Meta.read_only_fields + ("point",)
