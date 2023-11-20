from django.db.models import Model
from rest_framework.serializers import ModelSerializer

from meinberlin.apps.maptopicprio.models import MapTopic
from meinberlin.apps.maptopicprio.serializers import MapTopicSerializer
from meinberlin.apps.topicprio.api import BaseTopicViewSet
from meinberlin.apps.topicprio.api import ModuleMixin
from meinberlin.apps.topicprio.api import PermissionInfoMixin
from meinberlin.apps.topicprio.api import TopicFilterInfoMixin


class MapTopicViewSet(
    ModuleMixin, TopicFilterInfoMixin, PermissionInfoMixin, BaseTopicViewSet
):
    model: Model = MapTopic
    serializer_class: ModelSerializer = MapTopicSerializer
