import pytest
import requests_mock
from django.urls import reverse
from rest_framework import status

from meinberlin.apps.bplan import models as bplan_models


@pytest.mark.django_db
def test_initiator_add_bplan(apiclient, organisation):
    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "identifier": "VE69 5a BPLAN",
        "image_url": "https://example.org/image",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    # png
    with requests_mock.Mocker() as m, open(
        "tests/bplan/assets/image_100_500.png", "rb"
    ) as f:
        m.get("https://example.org/image", body=f)
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        bplan = bplan_models.Bplan.objects.first()
        assert bplan.tile_image.name.endswith(".png")
    # png with out extension
    with requests_mock.Mocker() as m, open(
        "tests/bplan/assets/image_100_500", "rb"
    ) as f:
        m.get("https://example.org/image", body=f)
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        bplan = bplan_models.Bplan.objects.first()
        assert bplan.tile_image.name.endswith(".png")
    # jpg
    with requests_mock.Mocker() as m, open(
        "tests/bplan/assets/image_100_500.jpg", "rb"
    ) as f:
        m.get("https://example.org/image", body=f)
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        bplan = bplan_models.Bplan.objects.first()
        assert bplan.tile_image.name.endswith(".jpg")
    # broken image
    with requests_mock.Mocker() as m, open("tests/bplan/assets/test.bin", "rb") as f:
        m.get("https://example.org/image", body=f)
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
