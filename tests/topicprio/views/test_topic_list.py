import pytest

from meinberlin.apps.topicprio import phases
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_list_view(client, phase_factory, topic_factory):
    phase, module, project, topic = setup_phase(
        phase_factory, topic_factory, phases.PrioritizePhase)
    phase_2, module_2, project_2, topic_2 = setup_phase(
        phase_factory, topic_factory, phases.PrioritizePhase)
    url = project.get_absolute_url()

    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_topicprio/topic_list.html')
        assert response.status_code == 200
        assert topic in response.context_data['topic_list']
        assert topic_2 not in response.context_data['topic_list']
        assert response.context_data['topic_list'][0].comment_count == 0
        assert (response.context_data['topic_list'][0]
                .positive_rating_count == 0)
        assert (response.context_data['topic_list'][0]
                .negative_rating_count == 0)
