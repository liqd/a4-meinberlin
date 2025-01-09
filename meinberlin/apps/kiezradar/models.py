from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.projects.models import Topic

Organisation = settings.A4_ORGANISATIONS_MODEL


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


class SearchProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_profiles",
    )
    name = models.CharField(max_length=255, null=True)
    number = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=True)
    disabled = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
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
                latest = SearchProfile.objects.filter(user=self.user).latest("number")
            except SearchProfile.DoesNotExist:
                pass
            self.number = latest.number + 1 if latest else 1
        super().save(update_fields=update_fields, *args, **kwargs)

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint("user", "number", name="unique-search-profile")
        ]
        indexes = [models.Index("number", name="searchprofile_number_idx")]

    def __str__(self):
        return f"kiezradar search profile - {self.name}, disabled {self.disabled}"
