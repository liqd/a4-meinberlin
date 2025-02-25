import pytest
from django.urls import reverse

from meinberlin.apps.kiezradar.models import KiezRadar


@pytest.mark.django_db
def test_anonymous_user_cannot_create_kiezradar(apiclient, geojson_point_str):
    payload = {"name": "Test Search Profile", "point": geojson_point_str, "radius": 500}

    url = reverse("kiezradar-list")
    response = apiclient.post(url, payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_user_can_create_kiezradar(user, apiclient, geos_point, geojson_point_str):
    payload = {"name": "My Kiez", "point": geojson_point_str, "radius": 600}
    apiclient.force_authenticate(user)
    url = reverse("kiezradar-list")
    response = apiclient.post(url, payload, format="json")

    assert response.status_code == 201
    assert KiezRadar.objects.count() == 1
    kiezradar = KiezRadar.objects.first()
    assert kiezradar.name == payload["name"]
    assert kiezradar.point.equals(geos_point)


@pytest.mark.django_db
def test_user_can_create_kiezradar_with_geo_data_as_dict(
    user, apiclient, geos_point, geojson_point
):
    payload = {"name": "My Kiez", "point": geojson_point, "radius": 600}
    apiclient.force_authenticate(user)
    url = reverse("kiezradar-list")
    response = apiclient.post(url, payload, format="json")

    assert response.status_code == 201
    assert KiezRadar.objects.count() == 1
    kiezradar = KiezRadar.objects.first()
    assert kiezradar.name == payload["name"]
    assert kiezradar.point.equals(geos_point)


@pytest.mark.django_db
def test_user_cannot_create_kiezradar_smaller_500(
    user, apiclient, geojson_point, geojson_point_str
):
    payload = {"name": "Too small Kiez", "point": geojson_point_str, "radius": 400}
    apiclient.force_authenticate(user)
    url = reverse("kiezradar-list")
    response = apiclient.post(url, payload, format="json")

    assert response.status_code == 400
    assert response.data["radius"]


@pytest.mark.django_db
def test_user_cannot_create_kiezradar_bigger_3000(
    user, apiclient, geojson_point, geojson_point_str
):
    payload = {"name": "Too big Kiez", "point": geojson_point_str, "radius": 3001}
    apiclient.force_authenticate(user)
    url = reverse("kiezradar-list")
    response = apiclient.post(url, payload, format="json")

    assert response.status_code == 400
    assert response.data["radius"]


@pytest.mark.django_db
def test_user_cannot_update_other_users_kiezradar(
    user, apiclient, geojson_point_str, kiez_radar_factory
):
    kiezradar = kiez_radar_factory()
    assert user != kiezradar.creator

    payload = {"name": "My Kiezradar", "point": geojson_point_str, "radius": 600}
    apiclient.force_authenticate(user)
    url = reverse("kiezradar-detail", kwargs={"pk": kiezradar.id})
    response = apiclient.patch(url, data=payload, format="json")

    assert response.status_code == 404

    response = apiclient.put(url, data=payload, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_can_update_kiezradar(
    apiclient, geos_point, geojson_point_str, kiez_radar_factory
):
    kiezradar = kiez_radar_factory()

    payload = {"name": "My Kiezradar", "point": geojson_point_str, "radius": 600}
    apiclient.force_authenticate(kiezradar.creator)
    url = reverse("kiezradar-detail", kwargs={"pk": kiezradar.id})
    response = apiclient.patch(url, data=payload, format="json")

    assert response.status_code == 200
    assert KiezRadar.objects.count() == 1
    kiezradar = KiezRadar.objects.first()
    assert kiezradar.name == payload["name"]
    assert kiezradar.point.equals(geos_point)


@pytest.mark.django_db
def test_user_can_only_list_their_kiezradars(user, apiclient, kiez_radar_factory):
    kiezradar = kiez_radar_factory()
    assert KiezRadar.objects.count() == 1

    apiclient.force_authenticate(user)
    url = reverse("kiezradar-detail", kwargs={"pk": kiezradar.id})
    response = apiclient.get(url, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_cannot_see_other_users_kiezradar(user, apiclient, kiez_radar_factory):
    kiez_radar_factory()
    assert KiezRadar.objects.count() == 1

    apiclient.force_authenticate(user)
    url = reverse("kiezradar-list")
    response = apiclient.get(url, format="json")
    assert response.status_code == 200
    assert len(response.data) == 0

    kiezradar = kiez_radar_factory(creator=user)
    assert KiezRadar.objects.count() == 2

    response = apiclient.get(url, format="json")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == kiezradar.name
