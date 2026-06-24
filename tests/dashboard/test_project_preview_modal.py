import pytest
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_project_preview_modal_view(client, project_factory, organisation):
    project = project_factory(organisation=organisation)
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:project-preview-modal",
        kwargs={
            "organisation_slug": organisation.slug,
            "project_slug": project.slug,
        },
    )

    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert_template_response(
        response, "meinberlin_projects/partials/project_preview_modal_htmx.html"
    )
    content = response.content.decode()
    assert "<html" not in content
    assert "project-preview-modal__toggle" in content
    assert "project-preview-iframe" in content
    assert "data-content-url" in content
    assert "project-preview-content" not in content
    assert (
        reverse(
            "a4dashboard:project-preview-content",
            kwargs={
                "organisation_slug": organisation.slug,
                "project_slug": project.slug,
            },
        )
        in content
    )


@pytest.mark.django_db
def test_project_preview_content_view(client, project_factory, organisation):
    project = project_factory(organisation=organisation, name="Preview Test Project")
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:project-preview-content",
        kwargs={
            "organisation_slug": organisation.slug,
            "project_slug": project.slug,
        },
    )

    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert_template_response(
        response, "meinberlin_projects/partials/project_preview_iframe.html"
    )
    content = response.content.decode()
    assert "<html" in content
    assert 'name="viewport"' in content
    assert "common_css.css" in content
    assert "berlin_css.css" in content
    assert 'id="layout-grid"' in content
    assert "Preview Test Project" in content
    assert response.headers.get("X-Frame-Options") != "DENY"
    assert "js-history-back" not in content


@pytest.mark.django_db
def test_project_preview_content_view_draft_banner(
    client, project_factory, organisation
):
    project = project_factory(organisation=organisation, is_draft=True)
    initiator = organisation.initiators.first()
    url = reverse(
        "a4dashboard:project-preview-content",
        kwargs={
            "organisation_slug": organisation.slug,
            "project_slug": project.slug,
        },
    )

    client.login(username=initiator.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert "info-box" in response.content.decode()


@pytest.mark.django_db
def test_project_detail_full_page_unchanged(client, project_factory, user):
    project = project_factory(name="Full Page Project")
    url = reverse("project-detail", kwargs={"slug": project.slug})

    client.login(username=user.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert_template_response(response, "meinberlin_projects/project_detail.html")
    assert "<html" in response.content.decode()
    assert "Full Page Project" in response.content.decode()


@pytest.mark.django_db
def test_preview_sidebar_renders_htmx_for_internal_project(
    project_factory, organisation
):
    project = project_factory(organisation=organisation)
    template = (
        "{% load i18n meinberlin_project_tags %}"
        '{% include "a4dashboard/includes/preview.html" %}'
    )
    content = render_template(
        template,
        {
            "project": project,
            "view": type("View", (), {"organisation": organisation})(),
        },
    )
    assert "hx-get" in content
    assert "/preview/modal/" in content
    assert "js-project-preview-trigger" in content


@pytest.mark.django_db
def test_preview_sidebar_renders_external_link_for_bplan(bplan_factory, organisation):
    bplan = bplan_factory(organisation=organisation, url="https://example.com/bplan")
    template = (
        "{% load i18n meinberlin_project_tags %}"
        '{% include "a4dashboard/includes/preview.html" %}'
    )
    content = render_template(
        template,
        {
            "project": bplan,
            "view": type("View", (), {"organisation": organisation})(),
        },
    )
    assert "hx-get" not in content
    assert 'target="_blank"' in content
    assert "https://example.com/bplan" in content


@pytest.mark.django_db
def test_project_actions_back_link_hidden_on_project_detail(
    client, project_factory, user
):
    project = project_factory(name="Back Link Test Project")
    url = reverse("project-detail", kwargs={"slug": project.slug})

    client.login(username=user.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert "js-history-back" not in response.content.decode()


@pytest.mark.django_db
def test_project_actions_back_link_shown_on_project_information(
    client, project_factory, user
):
    project = project_factory(name="Back Link Test Project")
    url = reverse("project-information", kwargs={"slug": project.slug})

    client.login(username=user.email, password="password")
    response = client.get(url)
    assert response.status_code == 200
    assert "js-history-back" in response.content.decode()


@pytest.mark.django_db
def test_project_preview_modal_view_forbidden_for_stranger(
    client, project_factory, organisation, user_factory
):
    project = project_factory(organisation=organisation)
    stranger = user_factory()
    url = reverse(
        "a4dashboard:project-preview-modal",
        kwargs={
            "organisation_slug": organisation.slug,
            "project_slug": project.slug,
        },
    )

    client.login(username=stranger.email, password="password")
    response = client.get(url)
    assert response.status_code == 403
