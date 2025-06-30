from functools import reduce
from typing import Optional

from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchVector
from django.db import connection
from django.db.models import Q
from django.db.models import QuerySet

from adhocracy4.projects.models import Project
from meinberlin.apps.plans.models import Plan

from .models import ProjectType
from .models import SearchProfile

Organisation = settings.A4_ORGANISATIONS_MODEL


def full_text_search(
    search_term: str,
    search_queryset: Optional[QuerySet[SearchProfile]] = None,
    language: str = "german",
) -> QuerySet[SearchProfile]:
    """
    Performs a full-text search on the given SearchProfile QuerySet.
    To be used with postgresql-only database connection.

    Args:
        search_term (str): The user-provided search input.
        search_queryset (Optional[QuerySet[SearchProfile]]):
            A base QuerySet to apply the search on (default: all SearchProfile records).
        language (str, optional): The PostgreSQL full-text search language configuration. Defaults to "german". If more languages need to be supported than german, the config would need a library like nltk to sanitize multiple languages.

    Returns:
        QuerySet[SearchProfile]: A queryset of matching search profiles.
    """

    # Default to all search profiles if no QuerySet is provided
    search_queryset = search_queryset or SearchProfile.objects.all()

    query = " or ".join(search_term.split())
    search_query = SearchQuery(query, search_type="websearch", config=language)

    search_queryset = search_queryset.annotate(
        search=SearchVector("query__text", config=language)
    )
    search_queryset = search_queryset.filter(
        Q(search=search_query) | Q(query__isnull=True)
    )
    return search_queryset


def sqlite_text_search(
    search_term: str,
    search_queryset: Optional[QuerySet[SearchProfile]] = None,
) -> QuerySet[SearchProfile]:
    """
    Filters search profiles based on a search term using partial matches (icontains).
    This is a hack to make full text search somewhat useful on sqlite database connections.

    Args:
        search_profiles (QuerySet): The queryset of SearchProfile to filter.
        search_term (str): The search term to use for filtering, split into individual words.

    Returns:
        QuerySet: The filtered queryset based on the search term.
    """
    search_queryset = search_queryset or SearchProfile.objects.all()

    query = reduce(
        lambda a, b: a | b,
        (
            Q(query__text__icontains=term)
            for term in search_term.split()
            if len(term) > 2
        ),
    )
    return search_queryset.filter(query | Q(query__isnull=True))


def filter_by_term(obj: Project | Plan) -> QuerySet[SearchProfile]:
    search_term = ""
    # f"{obj.name} {obj.description} {obj.organisation.name}"

    if isinstance(obj, Project):
        search_term = f"{obj.name} {obj.description} {obj.organisation.name}"

        if obj.administrative_district:
            search_term += f" {obj.administrative_district.name}"

        if hasattr(obj, "externalproject"):
            if hasattr(obj.externalproject, "bplan"):
                search_term += f" {obj.externalproject.bplan.identifier}"

    elif isinstance(obj, Plan):
        search_term = f"{obj.title} {obj.description} {obj.organisation.name}"

        if obj.district:
            search_term += f" {obj.district.name}"

    for topic in obj.topic_names:
        search_term += f" {topic}"

    if connection.vendor == "postgresql":
        search_profiles = full_text_search(search_term)
    else:
        search_profiles = sqlite_text_search(search_term)

    return search_profiles


def get_search_profile_filters_for_plan(plan: Plan) -> Q:
    status = 0
    if plan.status == Plan.STATUS_DONE:
        status = 2

    return (Q(status__status=status) | Q(status__isnull=True)) & (
        Q(project_types__participation=plan.participation)
        | Q(project_types__isnull=True)
    )


def get_search_profile_filters_for_project(project: Project) -> Q:
    status = 2
    if project.phases.active_phases():
        status = 0
    elif project.phases.future_phases():
        status = 1

    return (
        (
            Q(project_types__participation=ProjectType.PARTICIPATION_CONSULTATION)
            | Q(project_types__isnull=True)
        )
        & Q(plans_only=False)
        & (Q(status__status=status) | Q(status__isnull=True))
    )


def get_common_filters(obj: Project | Plan) -> Q:
    district = obj.district if isinstance(obj, Plan) else obj.administrative_district
    filters = (
        (Q(topics__in=obj.topics.all()) | Q(topics__isnull=True))
        & (Q(organisations__in=[obj.organisation]) | Q(organisations__isnull=True))
        & Q(disabled=False)
    )

    if obj.point:
        has_both_set = Q(districts__isnull=False) & Q(kiezradars__isnull=False)
        district_filter = Q(districts__in=[district])
        kiezradar_filter = Q(
            kiezradars__radius__gte=Distance("kiezradars__point", obj.point)
        )
        location_filter = has_both_set & (district_filter | kiezradar_filter) | (
            (district_filter | Q(districts__isnull=True))
            & (kiezradar_filter | Q(kiezradars__isnull=True))
        )
    else:
        # If the SearchProfile has a Kiezradar, but the project has no Point, then no match!
        location_filter = (Q(districts__in=[district]) | Q(districts__isnull=True)) & Q(
            kiezradars__isnull=True
        )
    return filters & location_filter


def get_search_profiles_for_obj(obj: Project | Plan) -> QuerySet[SearchProfile]:
    qs = filter_by_term(obj)
    if isinstance(obj, Plan):
        filters = get_search_profile_filters_for_plan(obj)
    else:
        filters = get_search_profile_filters_for_project(obj)

    return qs.filter(filters & get_common_filters(obj))
