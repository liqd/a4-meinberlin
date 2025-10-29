import pytest
from django.urls import reverse

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.offlineevents.phases import OfflineEventPhase

component_module = components.modules.get("module_offlineevent")


@pytest.mark.django_db
def test_module_component_edit_view(client, phase_factory, offline_event_item_factory):
    phase, module, project, item = setup_phase(
        phase_factory, offline_event_item_factory, OfflineEventPhase
    )
    initiator = module.project.organisation.initiators.first()
    url = component_module.get_base_url(module)
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert_template_response(
        response, "meinberlin_offlineevents/offlineevent_module_dashboard_form.html"
    )


@pytest.mark.django_db
def test_module_component_create_view(
    client, phase_factory, offline_event_item_factory
):
    """Test that posting to the view creates/updates an OfflineEventItem"""
    phase, module, project, item = setup_phase(
        phase_factory, offline_event_item_factory, OfflineEventPhase
    )
    # Item exists but with different values
    item.name = "Old Name"
    item.event_type = "Old Type"
    item.description = "Old description"
    item.save()

    initiator = module.project.organisation.initiators.first()
    url = reverse(
        "a4dashboard:offlineevent-module", kwargs={"module_slug": module.slug}
    )
    data = {
        "name": "Event Name",
        "event_type": "Workshop",
        "description": "Description text",
    }
    client.login(username=initiator.email, password="password")
    response = client.post(url, data)
    assert response.status_code == 302
    item.refresh_from_db()
    assert item.name == data.get("name")
    assert item.event_type == data.get("event_type")
    assert item.description == data.get("description")


@pytest.mark.django_db
def test_module_component_update_view(
    client, phase_factory, offline_event_item_factory
):
    phase, module, project, item = setup_phase(
        phase_factory, offline_event_item_factory, OfflineEventPhase
    )
    initiator = module.project.organisation.initiators.first()
    url = reverse(
        "a4dashboard:offlineevent-module", kwargs={"module_slug": module.slug}
    )
    data = {
        "name": "Updated Event Name",
        "event_type": "Updated Workshop",
        "description": "Updated description text",
    }
    client.login(username=initiator.email, password="password")
    response = client.post(url, data)
    assert response.status_code == 302
    item.refresh_from_db()
    assert item.name == data.get("name")
    assert item.event_type == data.get("event_type")
    assert item.description == data.get("description")
