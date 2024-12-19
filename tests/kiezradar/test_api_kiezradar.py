import pytest
from django.urls import reverse

from adhocracy4.projects.models import Topic
from meinberlin.apps.kiezradar.models import SearchProfile


@pytest.fixture
def setup_data(
    administrative_district_factory,
    kiezradar_query_factory,
    organisation_factory,
    project_type_factory,
):
    """Fixture to create required data for the test."""
    district = administrative_district_factory()
    query = kiezradar_query_factory()
    topic = Topic.objects.first()
    organisation = organisation_factory()
    project_type = project_type_factory()

    return {
        "districts": [district.id],
        "query": query.id,
        "organisations": [organisation.id],
        "topics": [topic.id],
        "project_types": [project_type.id],
    }


@pytest.mark.django_db
def test_create_search_profile(client, user, setup_data):
    """Test creating and updating a SearchProfile via the API."""
    client.login(email=user.email, password="password")

    payload = {
        "name": "Test Search Profile",
        "description": "A description for the filters profile.",
        "disabled": False,
        "status": SearchProfile.STATUS_ONGOING,
        "query": setup_data["query"],
        "districts": setup_data["districts"],
        "topics": setup_data["topics"],
        "organisation": setup_data["organisations"],
        "project_types": setup_data["project_types"],
    }

    url = reverse("searchprofiles-list")
    response = client.post(url, payload, format="json")

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["disabled"] == payload["disabled"]
    assert data["status"] == payload["status"]
    assert data["query"] == payload["query"]

    # Check if the object was created in the database
    search_profile = SearchProfile.objects.get(id=data["id"])
    assert search_profile.name == payload["name"]
    assert search_profile.description == payload["description"]
    assert search_profile.disabled == payload["disabled"]
    assert search_profile.status == payload["status"]
    assert search_profile.query.id == payload["query"]
    assert (
        list(search_profile.districts.values_list("id", flat=True))
        == payload["districts"]
    )
    assert list(search_profile.topics.values_list("id", flat=True)) == payload["topics"]
    assert (
        list(search_profile.project_types.values_list("id", flat=True))
        == payload["project_types"]
    )


@pytest.mark.django_db
def test_update_search_profile(client, user, setup_data, search_profile_factory):
    """Test updating a SearchProfile via the API."""

    search_profile = search_profile_factory()

    query_id = setup_data.pop("query")
    search_profile.query_id = query_id
    search_profile.save()

    client.login(email=user.email, password="password")

    # test full update

    payload = {
        "name": "Test Search Profile",
        "description": "A description for the filters profile.",
        "disabled": False,
        "status": SearchProfile.STATUS_DONE,
        "query_text": "updated query",
        "districts": setup_data["districts"],
        "topics": setup_data["topics"],
        "organisation": setup_data["organisations"],
        "project_types": setup_data["project_types"],
    }
    url = reverse("searchprofiles-detail", kwargs={"pk": search_profile.id})
    response = client.put(url, data=payload, content_type="application/json")
    data = response.json()

    assert response.status_code == 200

    # Check if the object was updated in the database
    search_profile = SearchProfile.objects.get(id=data["id"])
    assert search_profile.name == payload["name"]
    assert search_profile.description == payload["description"]
    assert search_profile.disabled == payload["disabled"]
    assert search_profile.status == payload["status"]
    assert search_profile.query.text == payload["query_text"]
    assert (
        list(search_profile.districts.values_list("id", flat=True))
        == payload["districts"]
    )
    assert list(search_profile.topics.values_list("id", flat=True)) == payload["topics"]
    assert (
        list(search_profile.project_types.values_list("id", flat=True))
        == payload["project_types"]
    )

    # test partial update

    payload = {
        "query_text": "partial updated query",
    }
    url = reverse("searchprofiles-detail", kwargs={"pk": search_profile.id})
    response = client.patch(url, data=payload, content_type="application/json")
    data = response.json()

    assert response.status_code == 200

    # Check if the object was updated in the database
    search_profile = SearchProfile.objects.get(id=data["id"])
    assert search_profile.query.text == payload["query_text"]
