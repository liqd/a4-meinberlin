from django.template.defaultfilters import truncatechars
from django.utils.html import strip_tags
from rest_framework import serializers

from adhocracy4.actions.models import Action


class ActionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    actor = serializers.CharField(source="actor.username", default="system")
    target_creator = serializers.CharField(
        source="target_creator.username", default=None
    )
    project = serializers.CharField(source="project.name")

    _cache = {}

    class Meta:
        model = Action
        exclude = (
            "obj_content_type",
            "obj_comment_creator",
            "description",
            "verb",
            "target_object_id",
            "obj_object_id",
            "public",
            "target_content_type",
        )

    def get_cached_trigger(self, obj):
        trigger = self._cache.setdefault(
            f"trigger-${obj.id}",
            obj.obj_content_type.get_object_for_this_type(pk=obj.obj_object_id),
        )

        return (trigger, trigger.__class__.__name__)

    def get_cached_target(self, obj):
        if not obj.target_content_type:
            return None

        target = self._cache.setdefault(
            f"target-${obj.id}",
            obj.target_content_type.get_object_for_this_type(pk=obj.target_object_id),
        )

        return target

    def get_body(self, obj):
        trigger, trigger_class = self.get_cached_trigger(obj)
        target = self.get_cached_target(obj)
        body = None

        if trigger_class == "ModeratorRemark":
            body = strip_tags(target.moderator_feedback_text.feedback_text)
        elif trigger_class == "Comment":
            body = trigger.notification_content
        elif trigger_class == "Rating":
            possible_attributes = ["notification_content", "name"]
            for attr in possible_attributes:
                if hasattr(target, attr):
                    body = getattr(target, attr)
                    break

        return truncatechars(body, 50) if body else None

    def get_link(self, obj):
        trigger, trigger_class = self.get_cached_trigger(obj)

        if trigger_class == "ModeratorRemark":
            return trigger.item.get_absolute_url()
        if trigger_class == "Rating":
            return trigger.content_object.get_absolute_url()
        if trigger_class == "Phase":
            return trigger.module.get_absolute_url()
        if hasattr(trigger, "get_absolute_url"):
            return trigger.get_absolute_url()
        return None

    def get_item(self, obj):
        if obj.type == "item":
            return None
        target = self.get_cached_target(obj)

        if target and hasattr(target, "name"):
            return target.name
        elif target and hasattr(target, "content_object"):
            return target.content_object.name
        return None

    def get_type(self, obj):
        trigger = self.get_cached_target(obj)
        if obj.type == "rating" and trigger.__class__.__name__ == "Proposal":
            return "support"
        if obj.type == "phase" and obj.verb == "schedule":
            return "phase_soon_over"
        if obj.type == "phase" and obj.verb == "start":
            return "phase_started"
        return obj.type
