import pytest
from dateutil.parser import parse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.dashboard2 import components
from meinberlin.apps.extprojects.phases import ExternalPhase
from tests.helpers import assert_dashboard_form_component_response

component = components.projects.get('external')


@pytest.mark.django_db
def test_edit_view(client, phase_factory, external_project, module_factory):
    module = module_factory(project=external_project)
    phase = phase_factory(phase_content=ExternalPhase(), module=module)
    initiator = external_project.organisation.initiators.first()
    url = component.get_base_url(external_project)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'name': 'name',
        'description': 'desc',
        'image_copyright': 'copyright',
        'tile_image_copyright': 'tile_copyright',
        'is_archived': False,
        'is_public': True,
        'url': 'https://foo.bar',
        'start_date_0': '2013-01-01',
        'start_date_1': '18:00',
        'end_date_0': '2013-01-10',
        'end_date_1': '18:00',

    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-external-project-edit'
    external_project.refresh_from_db()
    assert external_project.name == data.get('name')
    assert external_project.description == data.get('description')
    assert external_project.tile_image_copyright == \
        data.get('tile_image_copyright')
    assert external_project.is_archived == data.get('is_archived')
    assert external_project.is_public == data.get('is_public')
    assert external_project.url == data.get('url')
    phase.refresh_from_db()
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2013-01-10 17:00:00 UTC")
