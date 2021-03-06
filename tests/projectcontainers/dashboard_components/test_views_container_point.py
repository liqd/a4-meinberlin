import json

import pytest

from adhocracy4.dashboard import components
from meinberlin.test.helpers import assert_dashboard_form_component_response

component = components.projects.get('point')


@pytest.mark.django_db
def test_edit_view(client, project_container, administrative_district):
    initiator = project_container.organisation.initiators.first()
    url = component.get_base_url(project_container)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'administrative_district': administrative_district.pk,
        'point': '{"type":"Feature","properties":{},'
                 '"geometry":{"type":"Point",'
                 '"coordinates":[13.382721,52.512121]}}'
    }
    client.post(url, data)
    project_container.refresh_from_db()
    assert project_container.administrative_district == \
        administrative_district
    point = project_container.point
    data = json.loads(data.get('point'))

    for key in point.keys():
        assert point[key] == data[key]

    assert project_container.project_type == \
        'meinberlin_projectcontainers.ProjectContainer'
