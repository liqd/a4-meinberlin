import pytest

from meinberlin.apps.projects.utils import get_public_project_url


@pytest.mark.django_db
def test_get_public_project_url_bplan_uses_external_url(bplan_factory):
    bplan = bplan_factory(url="https://diplan.example.com/bplan/1")
    assert (
        get_public_project_url(bplan, base_url="https://mein.berlin.de")
        == "https://diplan.example.com/bplan/1"
    )


@pytest.mark.django_db
def test_get_public_project_url_bplan_without_external_url(bplan_factory):
    bplan = bplan_factory(url="")
    assert get_public_project_url(bplan, base_url="https://mein.berlin.de") == ""


@pytest.mark.django_db
def test_get_public_project_url_regular_project(project_factory):
    project = project_factory()
    assert get_public_project_url(project, base_url="https://mein.berlin.de") == (
        "https://mein.berlin.de" + project.get_absolute_url()
    )
