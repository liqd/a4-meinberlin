from django.db.models import Model
from rest_framework.serializers import ModelSerializer

from adhocracy4.api.mixins import ModuleMixin
from meinberlin.apps.contrib.mixins import MapPolygonMixin
from meinberlin.apps.ideas.api import BaseIdeaViewSet
from meinberlin.apps.ideas.api import IdeaFilterInfoMixin
from meinberlin.apps.ideas.api import PermissionInfoMixin
from meinberlin.apps.mapideas.models import MapIdea
from meinberlin.apps.mapideas.serializers import MapIdeaSerializer


class MapIdeaViewSet(
    ModuleMixin,
    MapPolygonMixin,
    IdeaFilterInfoMixin,
    PermissionInfoMixin,
    BaseIdeaViewSet,
):
    """Provides a basic ViewSet for MapIdeas."""

    model: Model = MapIdea
    serializer_class: ModelSerializer = MapIdeaSerializer
