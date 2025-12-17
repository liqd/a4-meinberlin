import pytest
from dateutil.parser import parse
from django.core import mail

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.bplan.phases import StatementPhase
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_group_members

BPLAN_REQUEST_DATA = {
    "name": "name",
    "description": "desc",
    "administrative_district": "mi",
    "image_copyright": "copyright",
    "tile_image_copyright": "tile_copyright",
    "is_archived": False,
    "is_public": True,
    "url": "https://foo.bar",
    "office_worker_email": "test@foo.bar",
    "start_date_0": "2013-01-01",
    "start_date_1": "18:00",
    "end_date_0": "2013-01-10",
    "end_date_1": "18:00",
}


@pytest.mark.django_db
def test_edit_view(client, phase_factory, bplan, module_factory):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    module = module_factory(project=bplan)
    phase = phase_factory(phase_content=StatementPhase(), module=module)
    initiator = bplan.organisation.initiators.first()
    url = components.projects["bplan"].get_base_url(bplan)
    client.login(username=initiator.email, password="password")

    # Test GET request
    response = client.get(url)
    assert_dashboard_form_component_response(response, components.projects["bplan"])
    assert len(mail.outbox) == 1

    # Test POST request
    response = client.post(url, BPLAN_REQUEST_DATA)
    assert redirect_target(response) == "dashboard-bplan-project-edit"

    # Verify data was saved correctly
    bplan.refresh_from_db()
    assert bplan.name == BPLAN_REQUEST_DATA.get("name")
    assert bplan.description == BPLAN_REQUEST_DATA.get("description")
    assert bplan.administrative_district.short_code == BPLAN_REQUEST_DATA.get(
        "administrative_district"
    )
    assert bplan.tile_image_copyright == BPLAN_REQUEST_DATA.get("tile_image_copyright")
    assert bplan.is_archived == BPLAN_REQUEST_DATA.get("is_archived")
    assert bplan.is_public == BPLAN_REQUEST_DATA.get("is_public")
    assert bplan.url == BPLAN_REQUEST_DATA.get("url")
    assert bplan.office_worker_email == BPLAN_REQUEST_DATA.get("office_worker_email")

    # Verify phase dates
    phase.refresh_from_db()
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2013-01-10 17:00:00 UTC")

    # Verify project type and emails
    assert bplan.project_type == "meinberlin_bplan.Bplan"
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to == ["test@foo.bar"]


@pytest.mark.django_db
def test_edit_view_group_member(
    client, phase_factory, bplan, module_factory, group_factory, user_factory
):
    district, _ = AdministrativeDistrict.objects.get_or_create(
        name="Mitte", short_code="mi"
    )

    module = module_factory(project=bplan)
    phase = phase_factory(phase_content=StatementPhase(), module=module)
    bplan, _, group_member_in_pro, _ = setup_group_members(
        bplan, group_factory, user_factory
    )
    url = components.projects["bplan"].get_base_url(bplan)
    client.login(username=group_member_in_pro.email, password="password")

    # Test GET request
    response = client.get(url)
    assert_dashboard_form_component_response(response, components.projects["bplan"])
    assert len(mail.outbox) == 1

    # Test POST request
    response = client.post(url, BPLAN_REQUEST_DATA)
    assert redirect_target(response) == "dashboard-bplan-project-edit"

    # Verify data was saved correctly
    bplan.refresh_from_db()
    assert bplan.name == BPLAN_REQUEST_DATA.get("name")
    assert bplan.description == BPLAN_REQUEST_DATA.get("description")
    assert bplan.administrative_district.short_code == BPLAN_REQUEST_DATA.get(
        "administrative_district"
    )
    assert bplan.tile_image_copyright == BPLAN_REQUEST_DATA.get("tile_image_copyright")
    assert bplan.is_archived == BPLAN_REQUEST_DATA.get("is_archived")
    assert bplan.is_public == BPLAN_REQUEST_DATA.get("is_public")
    assert bplan.url == BPLAN_REQUEST_DATA.get("url")
    assert bplan.office_worker_email == BPLAN_REQUEST_DATA.get("office_worker_email")

    # Verify phase dates
    phase.refresh_from_db()
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2013-01-10 17:00:00 UTC")

    # Verify project type and emails
    assert bplan.project_type == "meinberlin_bplan.Bplan"
    assert len(mail.outbox) == 2
    assert mail.outbox[1].to == ["test@foo.bar"]
