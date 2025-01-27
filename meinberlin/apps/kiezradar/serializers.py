from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from rest_framework import serializers

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.maps.mixins import PointSerializerMixin
from adhocracy4.projects.models import Topic
from meinberlin.apps.kiezradar.models import KiezRadar
from meinberlin.apps.kiezradar.models import KiezradarQuery
from meinberlin.apps.kiezradar.models import ProjectStatus
from meinberlin.apps.kiezradar.models import ProjectType
from meinberlin.apps.kiezradar.models import SearchProfile
from meinberlin.apps.organisations.models import Organisation


class KiezRadarSerializer(PointSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = KiezRadar
        geo_field = "point"
        fields = ["id", "creator", "name", "point", "radius"]
        read_only_fields = ["id", "creator"]

    def validate(self, data):
        """Ensure a user has no more than 5 kiezradar entries."""
        user = self.context["request"].user
        if user.kiezradar_set.count() >= self.Meta.model.KIEZRADAR_LIMIT:
            raise serializers.ValidationError(
                "Users can only have up to 5 kiezradar filters."
            )
        return data


class SearchProfileSerializer(serializers.ModelSerializer):
    """Serializer for the SearchProfile model."""

    kiezradar = (
        serializers.PrimaryKeyRelatedField(
            queryset=KiezRadar.objects.all(), required=False
        ),
    )
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
    status = serializers.PrimaryKeyRelatedField(
        queryset=ProjectStatus.objects.all(), many=True, allow_null=True, required=False
    )
    topics = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), many=True, allow_null=True, required=False
    )

    class Meta:
        model = SearchProfile
        fields = [
            "id",
            "creator",
            "name",
            "number",
            "description",
            "disabled",
            "notification",
            "plans_only",
            "status",
            "query",
            "query_text",
            "organisations",
            "districts",
            "project_types",
            "topics",
            "kiezradar",
        ]

        read_only_fields = ["id", "creator", "number"]

    def validate_kiezradar(self, instance):
        user = self.context["request"].user
        if not user.has_perm("meinberlin_kiezradar.change_kiezradar", instance):
            raise serializers.ValidationError("Permission denied")
        return instance

    def create(self, validated_data):
        # Pop one-to-many fields from validated_data
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
        representation["status"] = [
            {
                "id": project_status.id,
                "status": project_status.status,
                "name": project_status.get_status_display(),
            }
            for project_status in instance.status.all()
        ]

        topics_enum = import_string(settings.A4_PROJECT_TOPICS)
        representation["topics"] = [
            {"id": topic.id, "code": topic.code, "name": topics_enum(topic.code).label}
            for topic in instance.topics.all()
        ]
        representation["query_text"] = instance.query.text if instance.query else ""

        if not instance.name:
            representation["name"] = _("Searchprofile %d") % instance.number
        return representation
