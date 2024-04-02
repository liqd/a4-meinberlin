import pytest

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.maptopicprio import phases


@pytest.mark.django_db
def test_list_view(client, phase_factory, maptopic_factory, area_settings_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase
    )
    area_settings_factory(module=module)
    phase_2, module_2, project_2, maptopic_2 = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase
    )
    area_settings_factory(module=module_2)
    url = project.get_absolute_url()

    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(response, "meinberlin_maptopicprio/maptopic_list.html")
        assert response.context["project"] == project
        assert response.context["module"] == module
