import pytest
from meinberlin.apps.kiezradar.models import KiezRadarFilter, SearchProfile


# Define a GeoJSON point
geojson_point = {
    "type": "Feature",
    "properties": {},
    "geometry": {"type": "Point", "coordinates": [1.0, 1.0]},
}

@pytest.mark.django_db
def test_unique_kiezradar_filter_for_same_user(
    client, user_factory, project, module_factory, phase_factory
    ):
    # while a user can have several search profiles, these profiles should have unique filters
    module = module_factory(project=project)
    phase = phase_factory(module=module)
    user1 = user1 = user_factory(username="user1")
    user2 = user_factory(username="user2")

    search_profile1 = SearchProfile.objects.create(user=user1, name="Profile 1")
    search_profile2 = SearchProfile.objects.create(user=user2, name="Profile 2")

    kiezradar = geojson_point
    args = [user1, phase, kiezradar]
    kwargs = {
            "type": "popular"
            }
    search_profile1.add_filter(*args)
    search_profile2.add_filter(*args)

#    filter1 = Filter.objects.create(user=user1, phase=phase, kiezradar=kiezradar, topics="topic")
#    filter2 = Filter.objects.create(user=user2, phase=phase, kiezradar=kiezradar, topics="topic")

    # Attempt to add the same filter to another profile of user1 (should raise a ValidationError)
    with self.assertRaises(ValidationError):
        search_profile3 = SearchProfile.objects.create(user=user1, name="Profile 3")


