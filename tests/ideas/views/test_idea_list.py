import pytest

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas import phases


@pytest.mark.django_db
def test_list_view(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase
    )
    phase_2, module_2, project_2, idea_2 = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase
    )
    url = project.get_absolute_url()

    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(response, "meinberlin_ideas/idea_list.html")
        assert response.context["project"] == project
        assert response.context["module"] == module
