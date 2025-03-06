from functools import reduce
from typing import Optional

from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchVector
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import connection
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects.models import Project
from adhocracy4.projects.models import Topic

Organisation = settings.A4_ORGANISATIONS_MODEL


class KiezRadar(UserGeneratedContentModel):
    KIEZRADAR_LIMIT = 5

    name = models.CharField(max_length=125)
    point = gis_models.PointField(
        blank=True,
        null=True,
        verbose_name=_("Where can your address be located on a map?"),
        help_text=_(
            "Click inside the marked area "
            "or type in an address to set the marker. A set "
            "marker can be dragged when pressed."
        ),
    )
    radius = models.FloatField(
        validators=[MinValueValidator(500.0), MaxValueValidator(3000.0)],
        help_text=_("How long should be the radius area?"),
    )

    def save(self, update_fields=None, *args, **kwargs):
        if (
            self._state.adding
            and self.creator.kiezradar_set.count() >= self.KIEZRADAR_LIMIT
        ):
            raise ValidationError(
                f"Users can only have up to {self.KIEZRADAR_LIMIT} radius filters."
            )
        super().save(update_fields=update_fields, *args, **kwargs)


class KiezradarQuery(models.Model):
    text = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"kiezradar query - {self.text}"

    class Meta:
        verbose_name_plural = "queries"


class ProjectType(models.Model):
    PARTICIPATION_INFORMATION = 0
    PARTICIPATION_CONSULTATION = 1
    PARTICIPATION_COOPERATION = 2
    PARTICIPATION_DECISION_MAKING = 3
    PARTICIPATION_CHOICES = (
        (PARTICIPATION_INFORMATION, _("information (no participation)")),
        (PARTICIPATION_CONSULTATION, _("consultation")),
        (PARTICIPATION_COOPERATION, _("cooperation")),
        (PARTICIPATION_DECISION_MAKING, _("decision-making")),
    )
    participation = models.SmallIntegerField(
        choices=PARTICIPATION_CHOICES,
        verbose_name=_("Type"),
    )

    def __str__(self):
        return f"participation type - {self.participation}"


class ProjectStatus(models.Model):
    STATUS_ONGOING = 0
    STATUS_FUTURE = 1
    STATUS_DONE = 2
    STATUS_CHOICES = (
        (STATUS_ONGOING, _("running")),
        (STATUS_FUTURE, _("future")),
        (STATUS_DONE, _("done")),
    )

    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        verbose_name=_("Status"),
    )

    def __str__(self):
        return f"project status - {self.status}"


class SearchProfile(UserGeneratedContentModel):
    name = models.CharField(max_length=255, null=True)
    number = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
    disabled = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
    plans_only = models.BooleanField(default=False)
    query = models.ForeignKey(
        KiezradarQuery,
        models.SET_NULL,
        related_name="search_profiles",
        blank=True,
        null=True,
    )
    kiezradars = models.ManyToManyField(
        KiezRadar,
        related_name="search_profiles",
        blank=True,
    )
    status = models.ManyToManyField(
        ProjectStatus,
        related_name="search_profiles",
        blank=True,
    )
    organisations = models.ManyToManyField(
        Organisation,
        related_name="search_profiles",
        blank=True,
    )
    districts = models.ManyToManyField(
        AdministrativeDistrict,
        related_name="search_profiles",
        blank=True,
    )
    project_types = models.ManyToManyField(
        ProjectType,
        related_name="search_profiles",
        blank=True,
    )
    topics = models.ManyToManyField(
        Topic,
        related_name="search_profiles",
        blank=True,
    )

    def save(self, update_fields=None, *args, **kwargs):
        """Custom save() to add the next unused number per user on creation"""
        if self.number is None:
            latest = None
            try:
                latest = SearchProfile.objects.filter(creator=self.creator).latest(
                    "number"
                )
            except SearchProfile.DoesNotExist:
                pass
            self.number = latest.number + 1 if latest else 1
        super().save(update_fields=update_fields, *args, **kwargs)

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint("creator", "number", name="unique-search-profile")
        ]
        indexes = [models.Index("number", name="searchprofile_number_idx")]

    def __str__(self):
        return f"kiezradar search profile - {self.name}, disabled {self.disabled}"


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


def get_search_profiles_for_project(project: Project) -> QuerySet[SearchProfile]:
    status = 2
    if project.phases.active_phases():
        status = 0
    elif project.phases.future_phases():
        status = 1

    search_profiles = SearchProfile.objects.filter(
        (Q(topics__in=project.topics.all()) | Q(topics__isnull=True))
        & (Q(status__status=status) | Q(status__isnull=True))
        & Q(plans_only=False)
        & (Q(organisations__in=[project.organisation]) | Q(organisations__isnull=True))
        & (
            Q(districts__in=[project.administrative_district])
            | Q(districts__isnull=True)
        )
        & (
            Q(project_types__participation=ProjectType.PARTICIPATION_CONSULTATION)
            | Q(project_types__isnull=True)
        )
        & Q(disabled=False)
    )
    search_term = f"{project.name} {project.description} {project.organisation.name}"

    if project.administrative_district:
        search_term += f" {project.administrative_district.name}"
    for topic in project.topic_names:
        search_term += f" {topic}"

    if connection.vendor == "postgresql":
        search_profiles = full_text_search(search_term, search_queryset=search_profiles)
    else:
        search_profiles = sqlite_text_search(
            search_term, search_queryset=search_profiles
        )

    if project.point:
        search_profiles = search_profiles.filter(
            Q(kiezradars__radius__gte=Distance("kiezradars__point", project.point))
            | Q(kiezradars__isnull=True)
        )
    return search_profiles
