from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from adhocracy4.maps.fields import PointField


class KiezRadarFilter(models.Model):
    PHASE_CHOICES = [
        ('current', 'current'),
        ('past', 'past'),
    ]
#    ORDER_BY_CHOICES = [
#        ('created', 'Date'),
#        ('popularity', 'Popularity'),
#    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kiezradars"
    )

    # Fields corresponding to MeinBerlinProjectViewSet filters
    # query = models.TextField(blank=True, null=True)  # custom query for free text search
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES, blank=True, null=True)
    location = PointField(blank=True, null=True)
    topics = models.JSONField(blank=True, null=True)
	# order_by = models.CharField(max_length=50, choices=ORDER_BY_CHOICES, blank=True, null=True)  # better to do this in react

    def __str__(self):
        return f"kiezradar - {self.user.username}"


class SearchProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_profiles"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    kiezradars = models.ManyToManyField(KiezRadarFilter, related_name="search_profiles")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def add_filter(self, *args, **kwargs):
        """
        Adds a filter to the SearchProfile if no other SearchProfile of the
        same user already has the same filter.
        """
        # Retrieve or create the filter with the specified attributes for the current user
        kiezradar, created = KiezRadarFilter.objects.get_or_create(
                user=self.user,
                *args,
                **kwargs
                )
        # Check if this filter is already associated with another SearchProfile for this user
        if kiezradar.search_profiles.filter(user=self.user).exists():
            raise ValidationError(
                f"Kiezradar filter is already associated with another search profile for this user."
            )

        # Add the filter to this SearchProfile
        self.filters.add(kiezradar)
