import pytest
from django.urls import reverse

from adhocracy4.projects.models import Topic
from meinberlin.apps.kiezradar.models import KiezRadar
from meinberlin.apps.kiezradar.models import SearchProfile


@pytest.fixture
def setup_data(
    administrative_district_factory,
    kiezradar_query_factory,
    kiez_radar_factory,
    organisation_factory,
    project_type_factory,
    project_status_factory,
):
    """Fixture to create required data for the test."""
    district = administrative_district_factory()
    query = kiezradar_query_factory()
    kiezradar = kiez_radar_factory()
    topic = Topic.objects.first()
    organisation = organisation_factory()
    project_type = project_type_factory()
    project_status = project_status_factory()

    return {
        "districts": [district.id],
        "query": query.id,
        "kiezradar": kiezradar.id,
        "organisations": [organisation.id],
        "topics": [topic.id],
        "project_types": [project_type.id],
        "project_status": [project_status.id],
    }


@pytest.mark.django_db
def test_anonymous_user_cant_create_search_profile(apiclient, setup_data):
    """Test creating and updating a SearchProfile via the API."""
    payload = {
        "name": "Test Search Profile",
        "description": "A description for the filters profile.",
        "disabled": False,
        "status": setup_data["project_status"],
        "query": setup_data["query"],
        "kiezradar": setup_data["kiezradar"],
        "districts": setup_data["districts"],
        "topics": setup_data["topics"],
        "organisation": setup_data["organisations"],
        "project_types": setup_data["project_types"],
    }

    url = reverse("searchprofiles-list")
    response = apiclient.post(url, payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_cant_create_search_profile_with_other_users_kiezradar(
    apiclient, user, kiez_radar_factory, setup_data
):
    apiclient.force_authenticate(user)
    kiezradar = kiez_radar_factory()
    assert user is not kiezradar.creator

    payload = {
        "name": "Test Search Profile",
        "description": "A description for the filters profile.",
        "disabled": False,
        "status": setup_data["project_status"],
        "query": setup_data["query"],
        "kiezradar": setup_data["kiezradar"],
        "districts": setup_data["districts"],
        "topics": setup_data["topics"],
        "organisation": setup_data["organisations"],
        "project_types": setup_data["project_types"],
    }

    url = reverse("searchprofiles-list")
    response = apiclient.post(url, payload, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_search_profile_with_kiezradar(apiclient, setup_data):
    """Test creating and updating a SearchProfile via the API."""
    kiezradar_id = setup_data["kiezradar"]
    kiezradar = KiezRadar.objects.get(pk=kiezradar_id)
    user = kiezradar.creator
    apiclient.force_authenticate(user)

    payload = {
        "name": "Test Search Profile",
        "description": "A description for the filters profile.",
        "disabled": False,
        "status": setup_data["project_status"],
        "query": setup_data["query"],
        "kiezradar": setup_data["kiezradar"],
        "districts": setup_data["districts"],
        "topics": setup_data["topics"],
        "organisation": setup_data["organisations"],
        "project_types": setup_data["project_types"],
    }

    url = reverse("searchprofiles-list")
    response = apiclient.post(url, payload, format="json")

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == payload["name"]
    assert data["number"] == 1
    assert data["description"] == payload["description"]
    assert data["disabled"] == payload["disabled"]
    assert data["query"] == payload["query"]
    assert data["kiezradar"] == payload["kiezradar"]

    # Check if the object was created in the database
    search_profile = SearchProfile.objects.get(id=data["id"])
    assert search_profile.name == payload["name"]
    assert search_profile.description == payload["description"]
    assert search_profile.disabled == payload["disabled"]
    assert search_profile.query.id == payload["query"]
    assert search_profile.kiezradar.id == payload["kiezradar"]
    assert (
        list(search_profile.districts.values_list("id", flat=True))
        == payload["districts"]
    )
    assert list(search_profile.status.values_list("id", flat=True)) == payload["status"]
    assert list(search_profile.topics.values_list("id", flat=True)) == payload["topics"]
    assert (
        list(search_profile.project_types.values_list("id", flat=True))
        == payload["project_types"]
    )
    assert search_profile.kiezradar.creator == search_profile.creator


@pytest.mark.django_db
def test_create_and_update_search_profile_without_name(apiclient, user, setup_data):
    """Test creating and updating a SearchProfile without name via the API."""
    apiclient.force_authenticate(user)

    payload = {
        "description": "A description for the filters profile.",
        "disabled": False,
        "status": setup_data["project_status"],
        "query": setup_data["query"],
        "districts": setup_data["districts"],
        "topics": setup_data["topics"],
        "organisation": setup_data["organisations"],
        "project_types": setup_data["project_types"],
    }

    url = reverse("searchprofiles-list")
    response = apiclient.post(url, payload, format="json")

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Searchprofile 1"
    assert data["number"] == 1
    assert data["description"] == payload["description"]
    assert data["disabled"] == payload["disabled"]
    assert data["query"] == payload["query"]

    # Check if the object was created in the database
    search_profile = SearchProfile.objects.get(id=data["id"])
    assert search_profile.name is None
    assert search_profile.description == payload["description"]
    assert search_profile.disabled == payload["disabled"]
    assert search_profile.query.id == payload["query"]
    assert (
        list(search_profile.districts.values_list("id", flat=True))
        == payload["districts"]
    )
    assert list(search_profile.status.values_list("id", flat=True)) == payload["status"]
    assert list(search_profile.topics.values_list("id", flat=True)) == payload["topics"]
    assert (
        list(search_profile.project_types.values_list("id", flat=True))
        == payload["project_types"]
    )

    payload = {
        "name": "Test Search Profile",
    }
    url = reverse("searchprofiles-detail", kwargs={"pk": search_profile.id})
    response = apiclient.patch(url, data=payload, format="json")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == payload["name"]
    assert data["number"] == 1

    # Check if the object was updated in the database
    search_profile = SearchProfile.objects.get(id=data["id"])
    assert search_profile.name == payload["name"]


@pytest.mark.django_db
def test_user_cant_update_other_users_search_profile(
    apiclient, user, setup_data, search_profile_factory
):
    """Test updating a SearchProfile via the API."""

    search_profile = search_profile_factory()
    assert search_profile.creator != user
    apiclient.force_authenticate(user)

    payload = {
        "name": "Test Search Profile",
        "description": "A description for the filters profile.",
        "disabled": False,
        "status": setup_data["project_status"],
        "query_text": "updated query",
        "districts": setup_data["districts"],
        "topics": setup_data["topics"],
        "organisation": setup_data["organisations"],
        "project_types": setup_data["project_types"],
    }
    url = reverse("searchprofiles-detail", kwargs={"pk": search_profile.id})
    response = apiclient.put(url, data=payload, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_search_profile(
    apiclient, setup_data, kiez_radar_factory, search_profile_factory
):
    """Test updating a SearchProfile via the API."""

    search_profile = search_profile_factory()

    query_id = setup_data.pop("query")
    search_profile.query_id = query_id
    kiezradar_id = setup_data.pop("kiezradar")
    search_profile.kiezradar_id = kiezradar_id
    search_profile.save()

    apiclient.force_authenticate(search_profile.creator)

    # test full update

    new_kiezradar = kiez_radar_factory(creator=search_profile.creator)
    payload = {
        "name": "Test Search Profile",
        "description": "A description for the filters profile.",
        "disabled": False,
        "status": setup_data["project_status"],
        "kiezradar": new_kiezradar.id,
        "query_text": "updated query",
        "districts": setup_data["districts"],
        "topics": setup_data["topics"],
        "organisation": setup_data["organisations"],
        "project_types": setup_data["project_types"],
    }
    url = reverse("searchprofiles-detail", kwargs={"pk": search_profile.id})
    response = apiclient.put(url, data=payload, format="json")
    data = response.json()

    assert response.status_code == 200

    # Check if the object was updated in the database
    search_profile = SearchProfile.objects.get(id=data["id"])
    assert search_profile.name == payload["name"]
    assert search_profile.description == payload["description"]
    assert search_profile.disabled == payload["disabled"]
    assert search_profile.query.text == payload["query_text"]
    assert search_profile.kiezradar_id == payload["kiezradar"]
    assert (
        list(search_profile.districts.values_list("id", flat=True))
        == payload["districts"]
    )
    assert list(search_profile.topics.values_list("id", flat=True)) == payload["topics"]
    assert list(search_profile.status.values_list("id", flat=True)) == payload["status"]
    assert (
        list(search_profile.project_types.values_list("id", flat=True))
        == payload["project_types"]
    )

    # test partial update

    payload = {
        "query_text": "partial updated query",
    }
    url = reverse("searchprofiles-detail", kwargs={"pk": search_profile.id})
    response = apiclient.patch(url, data=payload, format="json")
    data = response.json()

    assert response.status_code == 200

    # Check if the object was updated in the database
    search_profile = SearchProfile.objects.get(id=data["id"])
    assert search_profile.query.text == payload["query_text"]


@pytest.mark.django_db
def test_creating_multiple_search_profiles_assign_correct_number(
    apiclient, user, setup_data
):
    """Test creating and updating a SearchProfile without name via the API."""
    apiclient.force_authenticate(user)

    payload = {
        "description": "A description for the filters profile.",
        "disabled": False,
        "status": setup_data["project_status"],
        "query": setup_data["query"],
        "districts": setup_data["districts"],
        "topics": setup_data["topics"],
        "organisation": setup_data["organisations"],
        "project_types": setup_data["project_types"],
    }

    url = reverse("searchprofiles-list")
    for i in range(1, 6):
        response = apiclient.post(url, payload, format="json")
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Searchprofile " + str(i)
        assert data["number"] == i

    assert SearchProfile.objects.count() == 5
    for i, search_profile in enumerate(SearchProfile.objects.all()):
        assert search_profile.name is None
        assert search_profile.number == i + 1


@pytest.mark.django_db
def test_user_can_only_list_their_searchprofiles(
    apiclient, user, setup_data, search_profile_factory
):
    search_profile = search_profile_factory(creator=user)
    search_profile1 = search_profile_factory(creator=user)
    search_profile_factory()
    search_profile_factory()

    apiclient.force_authenticate(user)

    url = reverse("searchprofiles-list")
    response = apiclient.get(url, format="json")
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["name"] == search_profile.name
    assert response.data[1]["name"] == search_profile1.name


@pytest.mark.django_db
def test_user_cant_see_other_users_searchprofile(
    apiclient, user, setup_data, search_profile_factory
):
    search_profile = search_profile_factory()

    apiclient.force_authenticate(user)

    url = reverse("searchprofiles-detail", kwargs={"pk": search_profile.pk})
    response = apiclient.get(url, format="json")
    assert response.status_code == 404
