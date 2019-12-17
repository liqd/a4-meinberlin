import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.test.helpers import assert_dashboard_form_component_response

component = components.projects.get('plans')


@pytest.mark.django_db
def test_edit_view(client, plan_factory, project_container):
    initiator = project_container.organisation.initiators.first()
    organisation = project_container.organisation
    plan = plan_factory(organisation=organisation)
    url = component.get_base_url(project_container)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'plans': plan.pk
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-plans-edit'
    project_container.refresh_from_db()
    assert list(project_container.plans.all()) == [plan]
    assert project_container.project_type == \
        'meinberlin_projectcontainers.ProjectContainer'
