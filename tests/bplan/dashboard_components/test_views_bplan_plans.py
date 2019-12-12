import pytest

from adhocracy4.dashboard import components
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.bplan.phases import StatementPhase
from meinberlin.test.helpers import assert_dashboard_form_component_response

component = components.projects.get('plans')


@pytest.mark.django_db
def test_edit_view(client, bplan, module_factory, phase_factory,
                   plan_factory):
    module = module_factory(project=bplan)
    phase_factory(phase_content=StatementPhase(), module=module)
    initiator = bplan.organisation.initiators.first()
    organisation = bplan.organisation
    plan = plan_factory(organisation=organisation)
    url = component.get_base_url(bplan)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'plans': plan.pk
    }
    response = client.post(url, data)
    assert redirect_target(response) == 'dashboard-plans-edit'
    bplan.refresh_from_db()
    assert list(bplan.plans.all()) == [plan]
    assert bplan.project_type == 'meinberlin_bplan.Bplan'
