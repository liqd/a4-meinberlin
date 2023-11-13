from django_filters import rest_framework as rest_filters

from adhocracy4.categories.models import Category
from adhocracy4.labels.models import Label
from meinberlin.apps.contrib.filters import DefaultsRestFilterSet
from meinberlin.apps.moderationtasks.filters import OpenTaskFilter
from meinberlin.apps.moderationtasks.models import ModerationTask
from meinberlin.apps.moderatorfeedback.models import (
    DEFAULT_CHOICES as moderator_status_default_choices,
)


class IdeaFilterSet(DefaultsRestFilterSet):
    """Base class which provides a FilterSet for ideas.

    Use with NoExceptionFilterBackend.
    """

    category = rest_filters.ModelChoiceFilter(queryset=Category.objects.all())
    labels = rest_filters.ModelChoiceFilter(queryset=Label.objects.all())
    moderator_status = rest_filters.ChoiceFilter(
        choices=moderator_status_default_choices
    )
    open_task = OpenTaskFilter(queryset=ModerationTask.objects.all())

    defaults = {}
