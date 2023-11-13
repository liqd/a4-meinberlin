from rest_framework import serializers

from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    negative_rating_count = serializers.SerializerMethodField()
    positive_rating_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Idea
        fields = (
            "additional_item_badges_for_list_count",
            "comment_count",
            "created",
            "creator",
            "get_moderator_status_display",
            "item_badges_for_list",
            "moderator_status",
            "modified",
            "name",
            "negative_rating_count",
            "pk",
            "positive_rating_count",
            "reference_number",
            "url",
        )
        read_only_fields = (
            "additional_item_badges_for_list_count",
            "comment_count",
            "created",
            "creator",
            "get_moderator_status_display",
            "item_badges_for_list",
            "moderator_status",
            "modified",
            "name",
            "negative_rating_count",
            "pk",
            "positive_rating_count",
            "reference_number",
            "url",
        )

    def get_creator(self, idea: Idea) -> str:
        return idea.creator.username

    def get_comment_count(self, idea: Idea) -> int:
        if hasattr(idea, "comment_count"):
            return idea.comment_count
        else:
            return 0

    def get_positive_rating_count(self, idea: Idea) -> int:
        if hasattr(idea, "positive_rating_count"):
            return idea.positive_rating_count
        else:
            return 0

    def get_negative_rating_count(self, idea: Idea) -> int:
        if hasattr(idea, "negative_rating_count"):
            return idea.negative_rating_count
        else:
            return 0

    def get_url(self, idea: Idea) -> str:
        return idea.get_absolute_url()

    def reference_number(self, idea: Idea) -> str:
        if hasattr(idea, "ref_number"):
            return idea.ref_number
        else:
            return ""
