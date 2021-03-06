import pytest

from adhocracy4.dashboard import components
from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import redirect_target
from meinberlin.test.helpers import assert_dashboard_form_component_response

component = components.projects.get('container-projects')


@pytest.mark.django_db
def test_edit_view(client, project_factory, project_container):
    initiator = project_container.organisation.initiators.first()
    organisation = project_container.organisation
    project = project_factory(access=Access.PUBLIC, organisation=organisation)
    url = component.get_base_url(project_container)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'projects': project.pk,
    }
    response = client.post(url, data)
    project_container.refresh_from_db()
    assert redirect_target(response) == 'dashboard-container-projects'
    assert list(project_container.projects.all()) == [project]
    assert project_container.project_type == \
        'meinberlin_projectcontainers.ProjectContainer'
