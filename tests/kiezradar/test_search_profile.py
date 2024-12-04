import pytest

from adhocracy4.projects.models import Topic


@pytest.mark.django_db
def test_create_search_profile(
    search_profile_factory,
    project_type_factory,
    kiezradar_query_factory,
    organisation_factory,
    administrative_district_factory,
):

    search_profile = search_profile_factory()
    assert search_profile.topics.all().count() == 0
    assert search_profile.districts.all().count() == 0
    assert search_profile.project_types.all().count() == 0
    assert search_profile.organisations.all().count() == 0

    topic1 = Topic.objects.first()
    topic2 = Topic.objects.last()
    search_profile.topics.add(topic1.id)
    search_profile.topics.add(topic2.id)
    assert search_profile.topics.all().count() == 2

    # adding same topic is not changing the profile's topics
    search_profile.topics.add(topic1.id)
    assert search_profile.topics.all().count() == 2
    assert topic1.id in [topic.id for topic in search_profile.topics.all()]

    participation1 = project_type_factory()
    participation2 = project_type_factory()
    search_profile.project_types.add(participation1.id)
    assert search_profile.project_types.all().count() == 1
    search_profile.project_types.add(participation2.id)
    assert search_profile.project_types.all().count() == 2
    assert participation2.id in [
        participation.id for participation in search_profile.project_types.all()
    ]

    organisation1 = organisation_factory()
    organisation2 = organisation_factory()
    search_profile.organisations.add(organisation1.id)
    search_profile.organisations.add(organisation2.id)
    assert search_profile.organisations.all().count() == 2

    district = administrative_district_factory()
    search_profile.districts.add(district.id)
    assert search_profile.districts.all().count() == 1

    query = kiezradar_query_factory()
    search_profile.query = query
    search_profile.save()
    assert search_profile.query == query
