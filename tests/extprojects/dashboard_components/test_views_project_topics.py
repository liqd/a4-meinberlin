import pytest
from django.conf import settings

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.test.helpers import assert_dashboard_form_component_response

component = components.projects.get('topics')


@pytest.mark.django_db
def test_edit_view(client, external_project):
    initiator = external_project.organisation.initiators.first()
    url = component.get_base_url(external_project)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    choices = settings.A4_PROJECT_TOPICS
    data = {
        'topics': choices[0][0],
    }

    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-topics-edit'
    external_project.refresh_from_db()
    assert external_project.topics == [data.get('topics')]
    assert external_project.project_type == \
        'meinberlin_extprojects.ExternalProject'
