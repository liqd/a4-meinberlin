import pytest

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.topicprio import phases


@pytest.mark.django_db
def test_list_view(client, phase_factory, topic_factory):
    phase, module, project, topic = setup_phase(
        phase_factory, topic_factory, phases.PrioritizePhase
    )
    phase_2, module_2, project_2, topic_2 = setup_phase(
        phase_factory, topic_factory, phases.PrioritizePhase
    )
    url = project.get_absolute_url()

    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(response, "meinberlin_topicprio/topic_list.html")
        assert response.context["project"] == project
        assert response.context["module"] == module
