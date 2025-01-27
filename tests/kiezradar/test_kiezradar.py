import pytest
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError

from meinberlin.apps.kiezradar.models import KiezRadar


@pytest.mark.django_db
def test_kiezradar_user_limit(user, kiez_radar_factory):
    kiezradar = kiez_radar_factory(creator=user)
    with pytest.raises(ValidationError) as error:
        for i in range(kiezradar.KIEZRADAR_LIMIT):
            kiez_radar_factory(creator=user)
        assert "Users can only have up to 5 radius filters." in error


@pytest.mark.django_db
def test_kiezradar_can_filter_by_distance_to_location1(user, kiez_radar_factory):
    kiez_location = Point(13.408151799858457, 52.51655612494057)
    kiez_location_small_radius = Point(13.408151799858457, 52.51655612494057)
    project_location = Point(13.409476102873219, 52.520861941592365, srid=4326)
    kiezradar_match = kiez_radar_factory(creator=user, point=kiez_location)
    kiez_radar_factory(creator=user, point=kiez_location_small_radius, radius=300)
    results = KiezRadar.objects.filter(radius__gte=Distance("point", project_location))
    assert len(results) == 1
    assert results[0] == kiezradar_match
