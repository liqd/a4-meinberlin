import pytest
from django.urls import reverse

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.topicprio import phases


@pytest.mark.django_db
def test_topic_list_mixins(apiclient, phase_factory, topic_factory):
    prioritize_phase, module, project, topic = setup_phase(
        phase_factory, topic_factory, phases.PrioritizePhase
    )

    url = reverse("topics-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)

    # permission info
    assert "permissions" in response.data
    with freeze_pre_phase(prioritize_phase):
        response = apiclient.get(url)
        assert response.data["permissions"]["view_rate_count"]
        assert response.data["permissions"]["view_comment_count"]

    with freeze_phase(prioritize_phase):
        response = apiclient.get(url)
        assert response.data["permissions"]["view_rate_count"]
        assert response.data["permissions"]["view_comment_count"]

    phase_factory(phase_content=phases.PrioritizePhase(), module=module)
    url = reverse("topics-list", kwargs={"module_pk": module.pk})
