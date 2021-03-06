import pytest

from adhocracy4.dashboard import components
from meinberlin.test.helpers import assert_dashboard_form_component_edited
from meinberlin.test.helpers import assert_dashboard_form_component_response

component = components.projects.get('container-basic')


@pytest.mark.django_db
def test_edit_view(client, project, project_container_factory):
    project_container = project_container_factory(projects=[project])
    initiator = project_container.organisation.initiators.first()
    url = component.get_base_url(project_container)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'name': 'name',
        'description': 'desc',
        'tile_image_copyright': 'tile_copyright',
        'is_archived': True,
    }
    response = client.post(url, data)
    assert_dashboard_form_component_edited(
        response, component, project_container, data)
    assert project_container.project_type == \
        'meinberlin_projectcontainers.ProjectContainer'
