import pytest
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.ideas import models
from meinberlin.apps.ideas import phases


@pytest.mark.django_db
def test_anonymous_cannot_create_idea(client, phase_factory):
    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        count = models.Idea.objects.all().count()
        assert count == 0
        response = client.get(url)
        assert response.status_code == 302
        assert redirect_target(response) == "account_login"


@pytest.mark.django_db
def test_user_can_create_idea_during_active_phase(
    client, phase_factory, user, category_factory
):
    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})

    with freeze_phase(phase):
        count = models.Idea.objects.all().count()
        assert count == 0
        client.login(username=user.email, password="password")
        response = client.get(url)
        assert_template_response(response, "meinberlin_ideas/idea_create_form.html")
        idea = {
            "name": "Idea",
            "description": "description",
            "category": category.pk,
        }
        response = client.post(url, idea)
        assert response.status_code == 302
        assert redirect_target(response) == "idea-detail"
        count = models.Idea.objects.all().count()
        assert count == 1


@pytest.mark.django_db
def test_user_cannot_create_idea_in_wrong_phase(client, phase_factory, user):
    phase = phase_factory(phase_content=phases.RatingPhase())
    module = phase.module
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        response = client.get(url)
        assert response.status_code == 302
        client.login(username=user.email, password="password")
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_idea_in_wrong_phase(
    client, phase_factory, category_factory, admin
):
    phase = phase_factory(phase_content=phases.RatingPhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        client.login(username=admin.email, password="password")
        response = client.get(url)
        assert_template_response(response, "meinberlin_ideas/idea_create_form.html")
        idea = {
            "name": "Idea",
            "description": "description",
            "category": category.pk,
        }
        response = client.post(url, idea)
        assert response.status_code == 302
        assert redirect_target(response) == "idea-detail"
        count = models.Idea.objects.all().count()
        assert count == 1


@pytest.mark.django_db
def test_idea_contact_can_be_skipped(client, phase_factory, user, category_factory):
    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        client.login(username=user.email, password="password")
        idea = {
            "name": "Idea",
            "description": "description",
            "category": category.pk,
            "allow_contact": False,
        }
        response = client.post(url, idea)
        assert response.status_code == 302
        assert redirect_target(response) == "idea-detail"
        idea = models.Idea.objects.get()
        assert idea.allow_contact is False
        assert idea.contact_email == ""


@pytest.mark.django_db
def test_idea_contact_with_account_email(client, phase_factory, user, category_factory):
    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        client.login(username=user.email, password="password")
        idea = {
            "name": "Idea",
            "description": "description",
            "category": category.pk,
            "allow_contact": True,
            "contact_email_0": user.email,
            "contact_phone": "0123456789",
            "contact_storage_consent": True,
        }
        response = client.post(url, idea)
        assert response.status_code == 302
        assert redirect_target(response) == "idea-detail"
        idea = models.Idea.objects.get()
        assert idea.allow_contact is True
        assert idea.contact_email == user.email
        assert idea.contact_phone == "0123456789"


@pytest.mark.django_db
def test_idea_contact_with_custom_email(client, phase_factory, user, category_factory):
    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        client.login(username=user.email, password="password")
        custom_email = "custom@example.com"
        idea = {
            "name": "Idea",
            "description": "description",
            "category": category.pk,
            "allow_contact": True,
            "contact_email_0": "other",
            "contact_email_1": custom_email,
            "contact_phone": "",
            "contact_storage_consent": True,
        }
        response = client.post(url, idea)
        assert response.status_code == 302
        assert redirect_target(response) == "idea-detail"
        idea = models.Idea.objects.get()
        assert idea.allow_contact is True
        assert idea.contact_email == custom_email


@pytest.mark.django_db
def test_idea_contact_requires_consent(client, phase_factory, user, category_factory):
    phase = phase_factory(phase_content=phases.IssuePhase())
    module = phase.module
    category = category_factory(module=module)
    url = reverse("meinberlin_ideas:idea-create", kwargs={"module_slug": module.slug})
    with freeze_phase(phase):
        client.login(username=user.email, password="password")
        idea = {
            "name": "Idea",
            "description": "description",
            "category": category.pk,
            "allow_contact": True,
            "contact_email_0": user.email,
            "contact_storage_consent": False,
        }
        response = client.post(url, idea)
        assert response.status_code == 200
        assert models.Idea.objects.all().count() == 0
