from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import serializers

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.projects.models import Topic
from meinberlin.apps.kiezradar.models import KiezradarQuery
from meinberlin.apps.kiezradar.models import ProjectType
from meinberlin.apps.kiezradar.models import SearchProfile
from meinberlin.apps.organisations.models import Organisation


class SearchProfileSerializer(serializers.ModelSerializer):
    """Serializer for the SearchProfile model."""

    query = (
        serializers.PrimaryKeyRelatedField(
            queryset=KiezradarQuery.objects.all(), required=False
        ),
    )
    query_text = serializers.CharField(required=False)
    organisations = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(), many=True, allow_null=True, required=False
    )
    districts = serializers.PrimaryKeyRelatedField(
        queryset=AdministrativeDistrict.objects.all(),
        many=True,
        allow_null=True,
        required=False,
    )
    project_types = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all(), many=True, allow_null=True, required=False
    )
    topics = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), many=True, allow_null=True, required=False
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = SearchProfile
        fields = [
            "id",
            "user",
            "name",
            "description",
            "disabled",
            "notification",
            "status",
            "status_display",
            "query",
            "query_text",
            "organisations",
            "districts",
            "project_types",
            "topics",
        ]

        read_only_fields = ["user"]

    def create(self, validated_data):
        # Pop many-to-many and one-to-many fields from validated_data
        query_text = validated_data.pop("query_text", None)

        if query_text:
            query, _ = KiezradarQuery.objects.get_or_create(text=query_text)
            validated_data["query"] = query

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Custom update to handle query fetching relationships.
        """
        # Pop many-to-many fields from validated_data
        query_text = validated_data.pop("query_text", None)

        # Update one-to-many relationship
        if query_text:
            # remove existing query and assign or create another
            query, _ = KiezradarQuery.objects.get_or_create(text=query_text)
            validated_data["query"] = query

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["organisations"] = [
            {"id": organisation.id, "name": organisation.name}
            for organisation in instance.organisations.all()
        ]
        representation["districts"] = [
            {"id": district.id, "name": district.name}
            for district in instance.districts.all()
        ]
        representation["project_types"] = [
            {"id": project_type.id, "name": project_type.get_participation_display()}
            for project_type in instance.project_types.all()
        ]

        topics_enum = import_string(settings.A4_PROJECT_TOPICS)
        representation["topics"] = [
            {"id": topic.id, "name": topics_enum(topic.code).label}
            for topic in instance.topics.all()
        ]
        return representation
