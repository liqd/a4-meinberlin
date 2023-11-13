from django_filters import rest_framework as rest_filters

from adhocracy4.categories.models import Category
from adhocracy4.labels.models import Label
from meinberlin.apps.contrib.filters import DefaultsRestFilterSet


class TopicFilterSet(DefaultsRestFilterSet):
    """Base class which provides a FilterSet for topics.
    Use with TopicFilterBackend.
    """

    category = rest_filters.ModelChoiceFilter(queryset=Category.objects.all())
    labels = rest_filters.ModelChoiceFilter(queryset=Label.objects.all())

    defaults = {}
