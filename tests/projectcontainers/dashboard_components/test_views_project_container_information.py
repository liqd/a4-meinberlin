import pytest

from meinberlin.apps.dashboard2 import components
from meinberlin.test.helpers import assert_dashboard_form_component_edited
from meinberlin.test.helpers import assert_dashboard_form_component_response

component = components.projects.get('container-information')


@pytest.mark.django_db
def test_edit_view(client, project, project_container_factory):
    project_container = project_container_factory(projects=[project])
    initiator = project_container.organisation.initiators.first()
    url = component.get_base_url(project_container)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'information': 'test',
    }
    response = client.post(url, data)
    assert_dashboard_form_component_edited(
        response, component, project_container, data)
