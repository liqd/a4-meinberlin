import pytest
from django.urls import reverse

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from meinberlin.apps.ideas import phases
from meinberlin.test.helpers import GuestUserCreator

WARNING_TEXT = "In order to take part in the project you have to"
INFO_TEXT = "You are participating as a guest"


@pytest.mark.django_db
def test_project_detail_shows_guest_warning_when_guests_disallowed(
    client, project_factory
):
    project = project_factory(
        access=Access.PUBLIC, is_draft=False, allow_guest_users=False
    )
    guest = GuestUserCreator().create_guest_user()
    client.force_login(guest)

    response = client.get(reverse("project-detail", kwargs={"slug": project.slug}))

    content = response.content.decode()
    assert response.status_code == 200
    assert "alert--warning" in content
    assert WARNING_TEXT in content
    assert reverse("guest_convert") in content
    assert reverse("account_logout") in content
    assert 'data-bs-dismiss="alert"' in content


@pytest.mark.django_db
def test_project_detail_shows_info_alert_when_guests_allowed(client, project_factory):
    project = project_factory(
        access=Access.PUBLIC, is_draft=False, allow_guest_users=True
    )
    guest = GuestUserCreator().create_guest_user()
    client.force_login(guest)

    response = client.get(reverse("project-detail", kwargs={"slug": project.slug}))

    content = response.content.decode()
    assert response.status_code == 200
    assert INFO_TEXT in content
    assert WARNING_TEXT not in content


@pytest.mark.django_db
def test_project_detail_hides_guest_alerts_for_regular_user(
    client, project_factory, user
):
    project = project_factory(
        access=Access.PUBLIC, is_draft=False, allow_guest_users=False
    )
    client.force_login(user)

    response = client.get(reverse("project-detail", kwargs={"slug": project.slug}))

    content = response.content.decode()
    assert response.status_code == 200
    assert INFO_TEXT not in content
    assert WARNING_TEXT not in content


@pytest.mark.django_db
def test_module_detail_shows_guest_warning_when_guests_disallowed(
    client, phase_factory
):
    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    project = module.project
    project.allow_guest_users = False
    project.save()
    guest = GuestUserCreator().create_guest_user()
    client.force_login(guest)

    with freeze_phase(phase):
        response = client.get(
            reverse("module-detail", kwargs={"module_slug": module.slug})
        )

    content = response.content.decode()
    assert response.status_code == 200
    assert "alert--warning" in content
    assert WARNING_TEXT in content


@pytest.mark.django_db
def test_guest_logout_switch_shows_personal_login_copy(client):
    guest = GuestUserCreator().create_guest_user()
    client.force_login(guest)

    response = client.get(reverse("account_logout"), {"guest_switch": "1"})

    assert response.status_code == 200
    assert response.context["guest_switch_logout"] is True
    assert "Log in with a personal account" in response.content.decode()
