import html

import pytest
from django.urls import reverse

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_react_delete_item_idea(rf, user, idea_factory):
    request = rf.get("/")
    request.user = user
    idea = idea_factory()
    module = idea.module
    template = "{% load react_delete_item %}{% react_delete_item item %}"
    context = {"request": request, "item": idea}

    api_url = reverse("items-detail", args=[idea.id])
    success_url = reverse("module-detail", args=[module.slug])
    rendered = html.unescape(render_template(template, context))

    assert rendered.startswith('<div data-mb-widget="delete-item"')
    assert api_url in rendered
    assert success_url in rendered
    assert '"itemType": "idea"' in rendered


@pytest.mark.django_db
def test_react_delete_item_proposal(rf, user, proposal_factory):
    request = rf.get("/")
    request.user = user
    proposal = proposal_factory()
    module = proposal.module
    template = "{% load react_delete_item %}{% react_delete_item item %}"
    context = {"request": request, "item": proposal}

    api_url = reverse("items-detail", args=[proposal.id])
    success_url = reverse("module-detail", args=[module.slug])
    rendered = html.unescape(render_template(template, context))

    assert rendered.startswith('<div data-mb-widget="delete-item"')
    assert api_url in rendered
    assert success_url in rendered
    assert '"itemType": "proposal"' in rendered
