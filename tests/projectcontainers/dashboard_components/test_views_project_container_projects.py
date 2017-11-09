import pytest

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.dashboard2 import components
from tests.helpers import assert_dashboard_form_component_response

component = components.projects.get('container-projects')


@pytest.mark.django_db
def test_edit_view(client, project_factory, project_container):
    initiator = project_container.organisation.initiators.first()
    url = component.get_base_url(project_container)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    project = project_factory(is_public=True)
    data = {
        'projects': project.pk,
    }
    response = client.post(url, data)
    project_container.refresh_from_db()
    assert redirect_target(response) == 'dashboard-container-projects'
    assert list(project_container.projects.all()) == [project]
