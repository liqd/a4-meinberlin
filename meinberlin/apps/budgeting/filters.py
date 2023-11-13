from django_filters import rest_framework as rest_filters

from meinberlin.apps.ideas.filters import IdeaFilterSet


class ProposalFilterSet(IdeaFilterSet):
    is_archived = rest_filters.BooleanFilter()
    defaults = {"is_archived": "false"}
