import pytest
from django.urls import reverse
from django.utils.translation import gettext as _

from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas import phases


def extract_data(response):
    data = response.context["pages"]

    return {
        "length": len(data),
        "first": data[0],
        "last": data[-1],
        "pages": data,
    }


@pytest.fixture()
def superuser_client(client, user_factory):
    admin = user_factory(is_superuser=True, is_staff=True)
    client.force_login(admin)
    return client


@pytest.mark.django_db
def test_render_breadcrumbs_kiezradar(client):
    data = extract_data(client.get("/kiezradar/"))

    assert data["length"] == 2
    assert data["first"]["title"] == _("Home page")
    assert data["first"]["url"] == "/"
    assert data["last"]["title"] == _("Kiezradar")
    assert data["last"]["url"] == "/kiezradar/"


@pytest.mark.django_db
def test_render_breadcrumbs_project(
    phase_factory,
    client,
):
    phase, module, project, item = setup_phase(phase_factory, None, phases.CollectPhase)
    data = extract_data(client.get(project.get_absolute_url()))

    assert data["length"] == 3
    assert data["first"]["title"] == _("Home page")
    assert data["first"]["url"] == "/"
    assert data["pages"][1]["title"] == _("Kiezradar")
    assert data["pages"][1]["url"] == "/kiezradar/"
    assert data["last"]["title"] == project.name
    assert data["last"]["url"] == project.get_absolute_url()


@pytest.mark.django_db
def test_render_breadcrumbs_plan(
    plan_factory,
    client,
):
    plan = plan_factory()
    data = extract_data(client.get(plan.get_absolute_url()))

    assert data["length"] == 3
    assert data["first"]["title"] == _("Home page")
    assert data["first"]["url"] == "/"
    assert data["pages"][1]["title"] == _("Kiezradar")
    assert data["pages"][1]["url"] == "/kiezradar/"
    assert data["last"]["title"] == plan.title
    assert data["last"]["url"] == plan.get_absolute_url()


@pytest.mark.django_db
def test_render_breadcrumbs_module_in_plan(
    plan_factory,
    phase_factory,
    client,
):
    phase, module, project, item = setup_phase(phase_factory, None, phases.CollectPhase)
    plan = plan_factory(projects=[project])
    data = extract_data(client.get(module.get_absolute_url()))

    assert data["length"] == 5
    assert data["pages"][2]["title"] == plan.title
    assert data["last"]["title"] == module.name
    assert data["last"]["url"] == module.get_absolute_url()


@pytest.mark.django_db
def test_render_breadcrumbs_module(
    phase_factory,
    client,
):
    phase, module, project, item = setup_phase(phase_factory, None, phases.CollectPhase)
    data = extract_data(client.get(module.get_absolute_url()))

    assert data["length"] == 4
    assert data["last"]["title"] == module.name
    assert data["last"]["url"] == module.get_absolute_url()


@pytest.mark.django_db
def test_render_breadcrumbs_item(
    phase_factory,
    idea_factory,
    client,
):
    phase, module, project, item = setup_phase(
        phase_factory, idea_factory, phases.CollectPhase
    )
    data = extract_data(client.get(item.get_absolute_url()))

    assert data["length"] == 5
    assert data["last"]["title"] == item.name
    assert data["last"]["url"] == item.get_absolute_url()


@pytest.mark.django_db
def test_render_breadcrumbs_item_edit(
    phase_factory,
    idea_factory,
    superuser_client,
):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.CollectPhase
    )
    url = reverse(
        "meinberlin_ideas:idea-update",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    data = extract_data(superuser_client.get(url))

    assert data["length"] == 6
    assert data["last"]["title"] == _("Edit idea")
    assert data["last"]["url"] == url


@pytest.mark.django_db
def test_render_breadcrumbs_item_moderate(
    phase_factory,
    idea_factory,
    superuser_client,
):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.CollectPhase
    )
    url = reverse(
        "meinberlin_ideas:idea-moderate",
        kwargs={"pk": idea.pk, "year": idea.created.year},
    )
    data = extract_data(superuser_client.get(url))

    assert data["length"] == 6
    assert data["last"]["title"] == _("Moderate idea")
    assert data["last"]["url"] == url


@pytest.mark.django_db
def test_render_breadcrumbs_item_create(
    phase_factory,
    idea_factory,
    superuser_client,
):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.CollectPhase
    )
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})
    data = extract_data(superuser_client.get(url))

    assert data["length"] == 5
    assert data["last"]["title"] == _("Create idea")
    assert data["last"]["url"] == url
