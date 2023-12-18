import json

import pytest
from django.urls import reverse
from django.utils import translation

from adhocracy4.test.helpers import freeze_pre_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.mapideas import phases


@pytest.mark.django_db
def test_map_idea_api(
    apiclient, area_settings_factory, module, map_idea_factory, phase_factory,
):
    phase_factory(phase_content=phases.CollectPhase(), module=module)
    area_settings_factory(module=module)

    idea = map_idea_factory(module=module)
    map_idea_factory(module=module)
    map_idea_factory(module=module)

    url = reverse("mapideas-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url + "?ordering=created")
    assert len(response.data["results"]) == 3
    assert response.data["results"][0]["pk"] == idea.pk
    assert response.data["results"][0]["point"] == idea.point


@pytest.mark.django_db
def test_idea_list_mixins(
    apiclient, area_settings_factory, phase_factory, map_idea_factory
):
    collect_phase, module, project, idea = setup_phase(
        phase_factory, map_idea_factory, phases.CollectPhase
    )
    area_settings_factory(module=module)
    url = reverse("mapideas-list", kwargs={"module_pk": module.pk})

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
        assert response.data["polygon"] == module.settings_instance.polygon
