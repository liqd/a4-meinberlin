import pytest
from django.contrib.gis.geos import Point
from django.db import connection

from adhocracy4.projects.models import Topic
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas.phases import CollectFeedbackPhase
from meinberlin.apps.kiezradar.models import ProjectStatus
from meinberlin.apps.kiezradar.models import ProjectType
from meinberlin.apps.kiezradar.models import SearchProfile
from meinberlin.apps.kiezradar.models import get_search_profiles_for_project


@pytest.mark.django_db
def test_create_search_profile(
    search_profile_factory,
    project_type_factory,
    kiez_radar_factory,
    kiezradar_query_factory,
    organisation_factory,
    administrative_district_factory,
):
    kiezradar = kiez_radar_factory()
    user = kiezradar.creator

    search_profile = search_profile_factory(creator=user)
    assert search_profile.query is None
    assert search_profile.kiezradars.all().count() == 0
    assert search_profile.topics.all().count() == 0
    assert search_profile.districts.all().count() == 0
    assert search_profile.project_types.all().count() == 0
    assert search_profile.organisations.all().count() == 0
    assert search_profile.number == 1

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

    search_profile.kiezradars.add(kiezradar.id)
    assert search_profile.kiezradars.first() == kiezradar
    assert search_profile.creator == kiezradar.creator


@pytest.mark.django_db
def test_search_profile_save_adds_number(
    user,
    search_profile_factory,
):
    user_2 = search_profile_factory().creator
    assert user is not user_2
    for i in range(5):
        search_profile_factory(creator=user)
    for i in range(2):
        search_profile_factory(creator=user_2)

    assert SearchProfile.objects.count() == 8
    for i, search_profile in enumerate(SearchProfile.objects.filter(creator=user)):
        assert search_profile.number == i + 1
    for i, search_profile in enumerate(SearchProfile.objects.filter(creator=user_2)):
        assert search_profile.number == i + 1


@pytest.mark.django_db
def test_searchprofile_filter_topics(phase_factory, search_profile_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase
    )
    topics = Topic.objects.all()
    project.topics.add(topics.first())
    project.topics.add(topics.last())

    search_profile = search_profile_factory()
    search_profile1 = search_profile_factory()
    search_profile2 = search_profile_factory()

    search_profile.topics.set([topics.first()])
    search_profile1.topics.set([list(topics)[2]])

    with freeze_phase(phase):
        result = get_search_profiles_for_project(project).order_by("pk")
        assert len(result) == 2
        assert result.first() == search_profile
        assert result.last() == search_profile2


@pytest.mark.django_db
def test_searchprofile_filter_project_status(phase_factory, search_profile_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase
    )
    search_profile = search_profile_factory(status=ProjectStatus.STATUS_ONGOING)
    search_profile1 = search_profile_factory(status=ProjectStatus.STATUS_DONE)
    search_profile2 = search_profile_factory(status=ProjectStatus.STATUS_ONGOING)
    assert search_profile1.status.first().status == ProjectStatus.STATUS_DONE

    with freeze_phase(phase):
        result = get_search_profiles_for_project(project).order_by("pk")
        assert len(result) == 2
        assert result.first() == search_profile
        assert result.last() == search_profile2
    with freeze_post_phase(phase):
        result = get_search_profiles_for_project(project)
        assert len(result) == 1
        assert result.first() == search_profile1


@pytest.mark.django_db
def test_searchprofile_filter_plan_only(phase_factory, search_profile_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase
    )
    search_profile = search_profile_factory()
    search_profile_factory(plans_only=True)
    search_profile2 = search_profile_factory()

    with freeze_phase(phase):
        result = get_search_profiles_for_project(project).order_by("pk")
        assert len(result) == 2
        assert result.first() == search_profile
        assert result.last() == search_profile2


@pytest.mark.django_db
def test_searchprofile_filter_organisation(
    phase_factory, search_profile_factory, organisation_factory
):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase
    )
    search_profile = search_profile_factory()
    search_profile.organisations.add(project.organisation)
    search_profile.organisations.add(organisation_factory())
    search_profile.organisations.add(organisation_factory())
    search_profile.organisations.count() == 3
    search_profile1 = search_profile_factory()
    search_profile1.organisations.add(organisation_factory())
    search_profile2 = search_profile_factory()

    with freeze_phase(phase):
        result = get_search_profiles_for_project(project).order_by("pk")
        assert len(result) == 2
        assert result.first() == search_profile
        assert result.last() == search_profile2


@pytest.mark.django_db
def test_searchprofile_filter_districts(
    phase_factory, search_profile_factory, administrative_district_factory
):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase
    )
    project.administrative_district = administrative_district_factory()
    search_profile = search_profile_factory()
    search_profile.districts.add(project.administrative_district)
    search_profile.districts.add(administrative_district_factory())
    search_profile.districts.add(administrative_district_factory())
    assert search_profile.districts.count() == 3
    search_profile1 = search_profile_factory()
    search_profile1.districts.add(administrative_district_factory())
    search_profile2 = search_profile_factory()

    with freeze_phase(phase):
        result = get_search_profiles_for_project(project).order_by("pk")
        assert len(result) == 2
        assert result.first() == search_profile
        assert result.last() == search_profile2


@pytest.mark.django_db
def test_searchprofile_filter_project_type(phase_factory, search_profile_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase
    )
    search_profile = search_profile_factory(
        project_types=ProjectType.PARTICIPATION_CONSULTATION
    )
    search_profile_factory(project_types=ProjectType.PARTICIPATION_COOPERATION)
    search_profile2 = search_profile_factory(
        project_types=ProjectType.PARTICIPATION_CONSULTATION
    )
    search_profile2.project_types.clear()

    with freeze_phase(phase):
        result = get_search_profiles_for_project(project).order_by("pk")
        assert len(result) == 2  # still two, because we also filter for isnull=True
        assert result.first() == search_profile


@pytest.mark.django_db
def test_searchprofile_filter_disabled(phase_factory, search_profile_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase
    )
    search_profile = search_profile_factory()
    search_profile_factory(disabled=True)
    search_profile2 = search_profile_factory()

    with freeze_phase(phase):
        result = get_search_profiles_for_project(project).order_by("pk")
        assert len(result) == 2
        assert result.first() == search_profile
        assert result.last() == search_profile2


@pytest.mark.django_db
def test_searchprofile_filter_query(
    phase_factory,
    search_profile_factory,
    kiezradar_query_factory,
    administrative_district_factory,
):
    phase, _, project, _ = setup_phase(
        phase_factory,
        None,
        CollectFeedbackPhase,
        module__project__name="Ein Projekt in der Hauptstadt Berlin",
    )
    topic1, topic2 = Topic.objects.first(), Topic.objects.last()
    project.topics.add(topic1)
    district = administrative_district_factory()
    project.description = "Eine Beschreibung des Projekts"
    project.administrative_district = district
    project.save()

    organisation = project.organisation
    organisation.name = "Liquid"
    organisation.save()

    # Create search profiles with associated queries
    berlin_profile = search_profile_factory(
        query=kiezradar_query_factory(text="Das ist Berlin")
    )
    search_profile_factory(query=kiezradar_query_factory(text="Das ist Leipzig"))
    other_profile = search_profile_factory(query=kiezradar_query_factory(text="Andere"))
    profile_without_query = search_profile_factory()
    search_profile_factory(
        query=kiezradar_query_factory(text="Berli")
    )  # partial word not matching
    stop_word_profile = search_profile_factory(
        query=kiezradar_query_factory(text="Ein Beispiel in der Zeitung")
    )
    organisation_name = search_profile_factory(
        query=kiezradar_query_factory(text="Liquid")
    )
    project_topic = search_profile_factory(
        query=kiezradar_query_factory(text=str(topic1))
    )
    search_profile_factory(query=kiezradar_query_factory(text=str(topic2)))
    project_description = search_profile_factory(
        query=kiezradar_query_factory(text="Beschreibung")
    )
    project_district = search_profile_factory(
        query=kiezradar_query_factory(text=district.name)
    )

    # Execute search
    with freeze_phase(phase):
        result = get_search_profiles_for_project(project).order_by("pk")

        if connection.vendor == "postgresql":
            expected_profiles = [
                berlin_profile,
                profile_without_query,
                organisation_name,
                project_topic,
                project_description,
                project_district,
            ]
        else:
            expected_profiles = [
                berlin_profile,
                other_profile,
                profile_without_query,
                stop_word_profile,
                organisation_name,
                project_topic,
                project_description,
                project_district,
            ]
        assert list(result) == expected_profiles


@pytest.mark.django_db
def test_searchprofile_filter_query_bplan(
    search_profile_factory,
    kiezradar_query_factory,
    bplan_factory,
):
    bplan = bplan_factory(identifier="B30-1 A30-bplan 2024")
    bplan_profile = search_profile_factory(
        query=kiezradar_query_factory(text="A30-bplan")
    )

    result = get_search_profiles_for_project(bplan).order_by("pk")
    assert list(result) == [bplan_profile]


@pytest.mark.django_db
def test_searchprofile_filter_kiezradar(
    user, phase_factory, search_profile_factory, kiez_radar_factory
):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase
    )
    project_location = Point(13.409476102873219, 52.520861941592365, srid=4326)
    project.point = project_location
    project.save()

    kiez_location = Point(13.408151799858457, 52.51655612494057)
    kiez_location_small_radius = Point(13.408151799858457, 52.51655612494057)
    kiezradar_match = kiez_radar_factory(creator=user, point=kiez_location)
    kiezradar_no_match = kiez_radar_factory(
        creator=user, point=kiez_location_small_radius, radius=300
    )

    search_profile = search_profile_factory()
    search_profile.kiezradars.add(kiezradar_match)
    search_profile1 = search_profile_factory()
    search_profile1.kiezradars.add(kiezradar_no_match)
    search_profile2 = search_profile_factory()

    with freeze_phase(phase):
        result = get_search_profiles_for_project(project).order_by("pk")
        assert len(result) == 2
        assert result.first() == search_profile
        assert result.last() == search_profile2
