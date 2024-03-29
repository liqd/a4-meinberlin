import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_group_members

component = components.projects.get("plans")


@pytest.mark.django_db
def test_edit_view(client, external_project, plan_factory):
    initiator = external_project.organisation.initiators.first()
    organisation = external_project.organisation
    plan = plan_factory(organisation=organisation)
    url = component.get_base_url(external_project)
    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {"plans": plan.pk}

    response = client.post(url, data)
    assert redirect_target(response) == "dashboard-plans-edit"
    external_project.refresh_from_db()
    assert list(external_project.plans.all()) == [plan]
    assert external_project.project_type == "meinberlin_extprojects.ExternalProject"


@pytest.mark.django_db
def test_edit_view_group_member(
    client, external_project, plan_factory, group_factory, user_factory
):
    external_project, _, group_member_in_pro, _ = setup_group_members(
        external_project, group_factory, user_factory
    )
    organisation = external_project.organisation
    plan = plan_factory(organisation=organisation)
    url = component.get_base_url(external_project)
    client.login(username=group_member_in_pro.email, password="password")
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {"plans": plan.pk}

    response = client.post(url, data)
    assert redirect_target(response) == "dashboard-plans-edit"
    external_project.refresh_from_db()
    assert list(external_project.plans.all()) == [plan]
    assert external_project.project_type == "meinberlin_extprojects.ExternalProject"
