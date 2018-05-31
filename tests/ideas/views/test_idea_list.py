import pytest

from meinberlin.apps.ideas import phases
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_list_view(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    phase_2, module_2, project_2, idea_2 = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    url = project.get_absolute_url()

    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_ideas/idea_list.html')
        assert response.status_code == 200
        assert idea in response.context_data['idea_list']
        assert idea_2 not in response.context_data['idea_list']
        assert response.context_data['idea_list'][0].comment_count == 0
        assert response.context_data['idea_list'][0].positive_rating_count == 0
        assert response.context_data['idea_list'][0].negative_rating_count == 0
