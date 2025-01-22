from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.maps.fields import PointField
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects.models import Topic

Organisation = settings.A4_ORGANISATIONS_MODEL


class KiezRadar(UserGeneratedContentModel):
    KIEZRADAR_LIMIT = 5

    name = models.CharField(max_length=125)
    point = PointField(
        blank=True,
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
        if self.creator.kiezradar_set.count() >= self.KIEZRADAR_LIMIT:
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
    STATUS_DONE = 1
    STATUS_FUTURE = 2
    STATUS_CHOICES = (
        (STATUS_ONGOING, _("running")),
        (STATUS_DONE, _("done")),
        (STATUS_FUTURE, _("future")),
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
    kiezradar = models.OneToOneField(
        KiezRadar,
        models.SET_NULL,
        related_name="search_profile",
        blank=True,
        null=True,
    )
    query = models.ForeignKey(
        KiezradarQuery,
        models.SET_NULL,
        related_name="search_profiles",
        blank=True,
        null=True,
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
