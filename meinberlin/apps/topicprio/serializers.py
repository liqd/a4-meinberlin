from rest_framework import serializers

from meinberlin.apps.topicprio.models import Topic


class TopicSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    negative_rating_count = serializers.SerializerMethodField()
    positive_rating_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = (
            "comment_count",
            "name",
            "negative_rating_count",
            "positive_rating_count",
            "pk",
            "url",
        )
        read_only_fields = (
            "comment_count",
            "name",
            "negative_rating_count",
            "positive_rating_count",
            "pk",
            "url",
        )

    def get_comment_count(self, topic: Topic) -> int:
        if hasattr(topic, "comment_count"):
            return topic.comment_count
        else:
            return 0

    def get_positive_rating_count(self, topic: Topic) -> int:
        if hasattr(topic, "positive_rating_count"):
            return topic.positive_rating_count
        else:
            return 0

    def get_negative_rating_count(self, topic: Topic) -> int:
        if hasattr(topic, "negative_rating_count"):
            return topic.negative_rating_count
        else:
            return 0

    def get_url(self, topic: Topic) -> str:
        return topic.get_absolute_url()
