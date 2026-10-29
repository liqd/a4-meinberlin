import pytest

from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases as budgeting_phases
from meinberlin.apps.ideas import phases as idea_phases
from meinberlin.apps.mapideas import phases as mapidea_phases


@pytest.mark.django_db
def test_back_button_hidden_on_item_detail_pages(
    client,
    user,
    phase_factory,
    idea_factory,
    map_idea_factory,
    proposal_factory,
    area_settings_factory,
):
    _, _, _, idea = setup_phase(phase_factory, idea_factory, idea_phases.CollectPhase)
    _, mapidea_module, _, mapidea = setup_phase(
        phase_factory, map_idea_factory, mapidea_phases.CollectPhase
    )
    area_settings_factory(module=mapidea_module)
    _, proposal_module, _, proposal = setup_phase(
        phase_factory, proposal_factory, budgeting_phases.CollectPhase
    )
    area_settings_factory(module=proposal_module)

    client.login(username=user.email, password="password")

    for item in (idea, mapidea, proposal):
        response = client.get(item.get_absolute_url())
        assert response.status_code == 200
        assert "js-history-back" not in response.content.decode()
