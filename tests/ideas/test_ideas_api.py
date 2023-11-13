import pytest
from django.urls import reverse
from django.utils import translation

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas import phases


@pytest.mark.django_db
def test_idea_list_mixins(apiclient, phase_factory, idea_factory):
    collect_phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.CollectPhase
    )

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)

    # locale info
    assert "locale" in response.data
    assert response.data["locale"] == translation.get_language()

    # permission info
    assert "permissions" in response.data
    with freeze_pre_phase(collect_phase):
        response = apiclient.get(url)
        assert not response.data["permissions"]["view_rate_count"]
        assert response.data["permissions"]["view_comment_count"]

    with freeze_phase(collect_phase):
        response = apiclient.get(url)
        assert not response.data["permissions"]["view_rate_count"]
        assert response.data["permissions"]["view_comment_count"]

    rating_phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.RatingPhase
    )
    phase_factory(phase_content=phases.CollectPhase(), module=module)
    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    with freeze_phase(rating_phase):
        response = apiclient.get(url)
        assert response.data["permissions"]["view_rate_count"]
        assert response.data["permissions"]["view_comment_count"]
