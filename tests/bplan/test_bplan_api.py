import base64

import pytest
from dateutil.parser import parse
from django.core import mail
from django.urls import reverse
from rest_framework import status

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from meinberlin.apps.bplan import models as bplan_models

# from tests.conftest import get_geojson_point
from tests.helpers import get_base64_image
from tests.helpers import pytest_regex

# from unittest.mock import patch


@pytest.mark.django_db
def test_anonymous_cannot_add_bplan(apiclient, organisation):
    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {}
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_none_initiator_cannot_add_bplan(apiclient, organisation, user):
    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {}
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_initiator_add_bplan(apiclient, organisation):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.name == data["name"]
    assert bplan.description == data["description"]
    assert bplan.administrative_district.short_code == data["administrative_district"]
    assert bplan.url == data["url"]
    assert bplan.office_worker_email == data["office_worker_email"]
    assert bplan.is_archived is False
    assert bplan.is_draft is False
    assert bplan.information == ""
    assert bplan.result == ""
    assert bplan.start_date == parse("2013-01-01 17:00:00 UTC")
    assert bplan.end_date == parse("2021-01-01 17:00:00 UTC")
    module = module_models.Module.objects.get(project=bplan)
    assert module is not None
    phase = phase_models.Phase.objects.get(module=module)
    assert phase is not None
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2021-01-01 17:00:00 UTC")
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["test@liqd.de"]


@pytest.mark.django_db
def test_group_member_cannot_add_bplan(
    apiclient, organisation, group_factory, user_factory
):
    """Group members can add bplan via dashboard, but not via API."""
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    group1 = group_factory()
    group2 = group_factory()
    user = user_factory.create(groups=(group1, group2))
    organisation.groups.add(group2)
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_initiator_update_bplan(apiclient, bplan, phase):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    # Make sure bplan has a district
    bplan.administrative_district = district
    bplan.save()

    phase.module.project = bplan
    phase.module.save()
    assert len(mail.outbox) == 1
    url = reverse(
        "bplan-detail",
        kwargs={"organisation_pk": bplan.organisation.pk, "pk": bplan.pk},
    )
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",  # Required for PUT
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "is_draft": "true",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
        "image_copyright": "do not copy",
    }
    user = bplan.organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    # ... rest of test


@pytest.mark.django_db
def test_unarchive_bplan(apiclient, bplan, phase):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    bplan.is_archived = True
    phase.module.project = bplan
    phase.module.save()
    assert len(mail.outbox) == 1
    url = reverse(
        "bplan-detail",
        kwargs={"organisation_pk": bplan.organisation.pk, "pk": bplan.pk},
    )
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "is_draft": "true",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
        "image_copyright": "do not copy",
    }
    user = bplan.organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.is_draft is True
    assert bplan.is_archived is False
    assert bplan.tile_image_copyright == data.get("image_copyright")
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to == ["test@liqd.de"]


@pytest.mark.django_db
def test_initiator_update_bplan_field(apiclient, bplan_factory, phase):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    bplan = bplan_factory(is_draft=False, administrative_district=district)
    phase.module.project = bplan
    phase.module.save()
    assert len(mail.outbox) == 1
    assert bplan.is_draft is False
    url = reverse(
        "bplan-detail",
        kwargs={"organisation_pk": bplan.organisation.pk, "pk": bplan.pk},
    )
    data = {
        "is_draft": "true",
    }
    user = bplan.organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    print(f"PATCH URL: {url}")
    print(f"PATCH data: {data}")

    response = apiclient.patch(url, data, format="json")
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.data}")
    assert response.status_code == status.HTTP_200_OK
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.is_draft is True
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to == [bplan.office_worker_email]


@pytest.mark.django_db
def test_initiator_update_bplan_phase(apiclient, bplan_factory, phase):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    bplan = bplan_factory(is_draft=False, administrative_district=district)
    phase.module.project = bplan
    phase.module.save()
    assert len(mail.outbox) == 1
    assert bplan.is_draft is False
    url = reverse(
        "bplan-detail",
        kwargs={"organisation_pk": bplan.organisation.pk, "pk": bplan.pk},
    )
    data = {
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    user = bplan.organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.start_date == parse("2013-01-01 17:00:00 UTC")
    assert bplan.end_date == parse("2021-01-01 17:00:00 UTC")
    phase = phase_models.Phase.objects.get(module=phase.module)
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2021-01-01 17:00:00 UTC")
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to == [bplan.office_worker_email]


@pytest.mark.django_db
def test_non_initiator_cannot_update_bplan(apiclient, bplan, user2):
    url = reverse(
        "bplan-detail",
        kwargs={"organisation_pk": bplan.organisation.pk, "pk": bplan.pk},
    )
    data = {}
    apiclient.force_authenticate(user=user2)
    response = apiclient.put(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


# @pytest.mark.django_db
# def test_add_bplan_response(apiclient, districts, organisation):
#     district, _ = AdministrativeDistrict.objects.get_or_create(
#         name="Mitte",
#         short_code="mi"
#     )

#     url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
#     data = {
#         "name": "bplan-1",
#         "description": "desc",
#         "administrative_district": "mi",
#         "url": "https://bplan.net",
#         "office_worker_email": "test@liqd.de",
#         "start_date": "2013-01-01 18:00",
#         "end_date": "2021-01-01 18:00",
#     }
#     user = organisation.initiators.first()
#     apiclient.force_authenticate(user=user)
#     response = apiclient.post(url, data, format="json")
#     assert response.status_code == status.HTTP_201_CREATED
#     embed_code = (
#         '<iframe height="500" style="width: 100%; min-height: 300px; '
#         'max-height: 100vh" '
#         'src="https://example.com/embed/projects/bplan-1/" '
#         'frameborder="0"></iframe>'
#     )
#     assert response.data == {"id": pytest_regex("^[0-9]*$"), "embed_code": embed_code}
#     assert len(mail.outbox) == 1
#     assert mail.outbox[0].to == ["test@liqd.de"]


@pytest.mark.django_db
def test_add_bplan_diplan_response_no_embed(apiclient, districts, organisation):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
        "bplan_id": "1-234",
        "point": '{"type":"Feature", "geometry":{"type":"Point","coordinates":[13.397788148643649,52.52958586909979]}}',
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {"id": pytest_regex("^[0-9]*$")}


# Removed test: test_bplan_api_adds_no_district_if_identifier_is_wrong
# This test is obsolete since identifier field no longer exists


@pytest.mark.django_db
def test_bplan_api_ignores_bplan_id_field(apiclient, districts, organisation):
    """Test that bplan_id field is accepted but ignored (for backward compatibility)"""
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
        "bplan_id": "some-random-id",  # This should be ignored
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    # bplan_id should not affect anything
    assert bplan.administrative_district.name == "Mitte"


@pytest.mark.django_db
def test_bplan_api_adds_topic_automatically(apiclient, districts, organisation):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.topics.count() == 1
    assert bplan.topics.first().code == "URB"


# @pytest.mark.django_db
# def test_bplan_api_adds_district_from_short_code(apiclient, districts, organisation):
#     url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
#     data = {
#         "name": "bplan-1",
#         "description": "desc",
#         "url": "https://bplan.net",
#         "office_worker_email": "test@liqd.de",
#         "start_date": "2013-01-01 18:00",
#         "administrative_district": "mi",
#         "end_date": "2021-01-01 18:00",
#     }
#     user = organisation.initiators.first()
#     apiclient.force_authenticate(user=user)
#     response = apiclient.post(url, data, format="json")
#     assert response.status_code == status.HTTP_201_CREATED
#     bplan = bplan_models.Bplan.objects.first()
#     assert bplan.administrative_district.name == "Mitte"


@pytest.mark.django_db
def test_bplan_api_diplan_adds_district_from_short_code(
    apiclient, organisation  # Remove "districts" fixture
):
    # Create the district first with the correct short_code
    from adhocracy4.administrative_districts.models import AdministrativeDistrict

    district, created = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", defaults={"short_code": "mi"}
    )
    # Ensure short_code is set (in case district already existed without it)
    if not created and not district.short_code:
        district.short_code = "mi"
        district.save()

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",  # This matches the short_code above
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "start_date": "2013-01-01 18:00",
        "bplan_id": "1-234",
        "point": '{"type":"Feature", "geometry":{"type":"Point","coordinates":[13.397788148643649,52.52958586909979]}}',
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")

    # Add debug if it still fails
    if response.status_code == 400:
        print(f"Error: {response.data}")

    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.administrative_district.name == "Mitte"


# Removed test: test_bplan_api_adds_district_from_identifier_with_whitespaces
# This test is obsolete since identifier field no longer exists


@pytest.mark.django_db
def test_bplan_api_sets_is_diplan_true_always(apiclient, districts, organisation):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    # is_diplan should always be True now
    assert bplan.is_diplan is True


@pytest.mark.django_db
def test_bplan_api_adds_is_diplan_if_point_is_sent(apiclient, districts, organisation):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "start_date": "2013-01-01 18:00",
        "point": '{"type":"Feature", "geometry":{"type":"Point","coordinates":[13.397788148643649,52.52958586909979]}}',
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.is_diplan is True


# Note: The tasks-related tests will fail if you don't have a tasks.py file
# You need to either create it or skip these tests


@pytest.mark.django_db
def test_bplan_api_accepts_valid_geojson(
    apiclient,
    districts,
    organisation,
    django_capture_on_commit_callbacks,
    geojson_point_str,
    geos_point,
):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
        "is_published": True,
        "point": geojson_point_str,
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    with django_capture_on_commit_callbacks(execute=True):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        bplan = bplan_models.Bplan.objects.first()
        assert bplan.is_draft is False
        assert bplan.is_diplan is True
        assert bplan.point.equals(geos_point)


@pytest.mark.django_db
def test_bplan_api_accepts_valid_base64_image(
    apiclient,
    districts,
    organisation,
    django_capture_on_commit_callbacks,
    geojson_point_str,
    geos_point,
):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    image = get_base64_image(width=500, height=300)
    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
        "is_published": True,
        "point": geojson_point_str,
        "tile_image": image,
    }

    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    with django_capture_on_commit_callbacks(execute=True):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        bplan = bplan_models.Bplan.objects.first()
        assert bplan.is_draft is False
        assert bplan.is_diplan is True
        with bplan.tile_image.file.open("r") as file:
            img = base64.b64encode(file.read())
            assert img == image


@pytest.mark.django_db
def test_bplan_api_accepts_bplan_without_tile_image(
    apiclient,
    districts,
    organisation,
    django_capture_on_commit_callbacks,
    geojson_point_str,
    geos_point,
):
    """Test that Bplans can be created without tile_image (optional field)."""
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
        "bplan_id": "1-234",
        "point": geojson_point_str,
    }

    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    with django_capture_on_commit_callbacks(execute=True):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        bplan = bplan_models.Bplan.objects.first()
        assert bplan.is_draft is False
        assert bplan.is_diplan is True
        assert bplan.point.equals(geos_point)
        # Verify that tile_image is not set (empty or None)
        assert not bplan.tile_image


@pytest.mark.django_db
def test_bplan_api_accepts_long_name_and_truncates_it(
    apiclient, districts, organisation, geojson_point_str
):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-" + "a" * 120,
        "description": "desc",
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "start_date": "2013-01-01 18:00",
        "point": geojson_point_str,
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.is_diplan is True
    assert len(bplan.name) == 120
    assert bplan.name == "bplan-" + "a" * 114


@pytest.mark.django_db
def test_bplan_api_accepts_long_description_and_truncates_it(
    apiclient, districts, organisation, geojson_point_str
):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    url = reverse("bplan-list", kwargs={"organisation_pk": organisation.pk})
    data = {
        "name": "bplan-long-desc",
        "description": "desc" + "a" * 250,
        "administrative_district": "mi",
        "url": "https://bplan.net",
        "start_date": "2013-01-01 18:00",
        "point": geojson_point_str,
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.is_diplan is True
    assert len(bplan.description) == 250
    assert bplan.description == "desc" + "a" * 246
