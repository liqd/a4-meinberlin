import pytest
from django.conf import settings

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.test.helpers import assert_dashboard_form_component_response

component = components.projects.get('topics')


@pytest.mark.django_db
def test_edit_view(client, project_container):
    initiator = project_container.organisation.initiators.first()
    url = component.get_base_url(project_container)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    choices = settings.A4_PROJECT_TOPICS
    data = {
        'topics': choices[0][0],
    }

    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-topics-edit'
    project_container.refresh_from_db()
    assert project_container.topics == [data.get('topics')]
    assert project_container.project_type == \
        'meinberlin_projectcontainers.ProjectContainer'
