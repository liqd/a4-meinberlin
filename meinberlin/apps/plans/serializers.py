from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from adhocracy4.maps.mixins import PointSerializerMixin
from adhocracy4.projects.enums import Access
from meinberlin.apps import logger
from meinberlin.apps.projects.serializers import CommonFields

from .models import Plan


class PlanSerializer(PointSerializerMixin, serializers.ModelSerializer, CommonFields):
    created_or_modified = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    published_projects_count = serializers.SerializerMethodField()
    subtype = serializers.ReadOnlyField(default="plan")
    tile_image = serializers.SerializerMethodField()
    tile_image_alt_text = serializers.SerializerMethodField()
    tile_image_copyright = serializers.SerializerMethodField()
    topics = serializers.SerializerMethodField()
    type = serializers.ReadOnlyField(default="plan")
    url = serializers.SerializerMethodField()

    def get_geojson_properties(self):
        return {"strname": "street_name", "hsnr": "house_number", "plz": "zip_code"}

    class Meta:
        model = Plan
        geo_field = "point"
        fields = [
            "cost",
            "created_or_modified",
            "district",
            "organisation",
            "participation",
            "participation_active",
            "participation_string",
            "point",
            "point_label",
            "published_projects_count",
            "status",
            "subtype",
            "tile_image",
            "tile_image_alt_text",
            "tile_image_copyright",
            "title",
            "topics",
            "type",
            "url",
        ]
        read_only_fields = ["point"]

    def get_topics(self, instance):
        return [topic.code for topic in instance.topics.all()]

    def get_url(self, instance: Plan) -> str:
        return instance.get_absolute_url()

    def get_published_projects_count(self, instance: Plan) -> int:
        """
        This method counts published projects of `instance`.
        It assumes that the related field `instance.projects` has been prefetched (see `plans/api.py`)
        and counts in Python (which is faster than hitting the db with `projects.count()`).
        For details, see `docs/performance_of_plans_serializer.py`.
        """

        count = 0
        for project in instance.projects.all():
            if project.is_draft or project.is_archived:
                continue
            if project.access in [Access.PUBLIC, Access.SEMIPUBLIC]:
                count += 1

        return count

    def get_participation_string(self, instance: Plan) -> str:
        return instance.get_status_display()

    def get_participation_active(self, instance: Plan) -> bool:
        return not bool(instance.status)

    def get_tile_image(self, instance: Plan) -> str:
        image_url = ""
        try:
            if instance.tile_image:
                image = get_thumbnailer(instance.tile_image)["project_tile"]
                image_url = image.url
            elif instance.image:
                image = get_thumbnailer(instance.image)["project_tile"]
                image_url = image.url
        except Exception as e:
            logger.warning(f"{e} issue with the image for plan {instance.title}")
            pass
        return image_url

    def get_tile_image_alt_text(self, instance: Plan) -> str:
        if instance.tile_image:
            return instance.tile_image_alt_text
        elif instance.image_alt_text:
            return instance.image_alt_text
        else:
            return ""

    def get_tile_image_copyright(self, instance: Plan) -> str:
        if instance.tile_image:
            return instance.tile_image_copyright
        elif instance.image_copyright:
            return instance.image_copyright
        else:
            return ""
