import pytest
from django.urls import reverse

from meinberlin.test.factories.ideas import IdeaFactory


@pytest.fixture
def moderated_project(project_factory, user):
    return project_factory(moderators=[user])


@pytest.mark.django_db
def test_dashboard_lists_moderated_projects(client, user, moderated_project):
    client.login(username=user.email, password="password")

    response = client.get(reverse("a4moderation:dashboard"))

    assert response.status_code == 200
    assert moderated_project in response.context["moderated_projects"]


@pytest.mark.django_db
def test_dashboard_is_empty_for_non_moderator(client, user2):
    client.login(username=user2.email, password="password")

    response = client.get(reverse("a4moderation:dashboard"))

    assert response.status_code == 200
    assert list(response.context["moderated_projects"]) == []


@pytest.mark.django_db
def test_project_view_lists_ideas_and_comments(
    client, user, moderated_project, module_factory, comment_factory
):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, name="My moderated idea")
    comment_factory(content_object=idea, comment="My moderated comment")
    client.login(username=user.email, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk}),
        {"state": "all"},
    )

    assert response.status_code == 200
    assert "My moderated idea" in response.content.decode()
    assert "My moderated comment" in response.content.decode()
    assert "moderation-item__menu" in response.content.decode()


@pytest.mark.django_db
def test_project_view_forbidden_for_non_moderator(client, user2, moderated_project):
    client.login(username=user2.email, password="password")

    response = client.get(
        reverse("a4moderation:project", kwargs={"project_pk": moderated_project.pk})
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_mark_idea_as_read(client, user, moderated_project, module_factory):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, is_reviewed=False)
    client.login(username=user.email, password="password")

    response = client.post(
        reverse(
            "a4moderation:item-read",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "meinberlin_ideas.idea",
                "pk": idea.pk,
            },
        ),
        {"read": "1", "state": "all"},
        HTTP_HX_REQUEST="true",
    )

    idea.refresh_from_db()
    assert response.status_code == 200
    assert idea.is_reviewed is True


@pytest.mark.django_db
def test_moderation_link_in_navigation_for_moderator(client, user, moderated_project):
    client.login(username=user.email, password="password")

    response = client.get(reverse("a4moderation:dashboard"))

    assert reverse("a4moderation:dashboard") in response.content.decode()


@pytest.mark.django_db
def test_group_member_sees_group_projects(client, user, group_factory, project_factory):
    group = group_factory()
    user.groups.add(group)
    group_project = project_factory(group=group)
    other_project = project_factory()
    client.login(username=user.email, password="password")

    response = client.get(reverse("a4moderation:dashboard"))

    projects = list(response.context["moderated_projects"])
    assert group_project in projects
    assert other_project not in projects


@pytest.mark.django_db
def test_organisation_initiator_sees_organisation_projects(
    client, user, organisation, project_factory
):
    organisation.initiators.add(user)
    project = project_factory(organisation=organisation)
    other_project = project_factory()
    client.login(username=user.email, password="password")

    response = client.get(reverse("a4moderation:dashboard"))

    projects = list(response.context["moderated_projects"])
    assert project in projects
    assert other_project not in projects


@pytest.mark.django_db
def test_save_feedback_from_dashboard(client, user, moderated_project, module_factory):
    module = module_factory(project=moderated_project)
    idea = IdeaFactory(module=module, is_reviewed=False)
    client.login(username=user.email, password="password")

    response = client.post(
        reverse(
            "a4moderation:item-feedback",
            kwargs={
                "project_pk": moderated_project.pk,
                "item_type": "meinberlin_ideas.idea",
                "pk": idea.pk,
            },
        ),
        {
            "moderator_status": "ACCEPTED",
            "feedback_text": "Sehr gute Idee",
            "state": "unread",
        },
        HTTP_HX_REQUEST="true",
    )

    idea.refresh_from_db()
    assert response.status_code == 200
    assert response["HX-Retarget"]
    assert idea.moderator_status == "ACCEPTED"
    assert "Sehr gute Idee" in idea.moderator_feedback_text.feedback_text
    assert idea.is_reviewed is True
