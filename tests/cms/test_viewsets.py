import pytest
from dateutil.parser import parse
from django.utils import timezone
from freezegun import freeze_time

from adhocracy4.projects.models import Project
from meinberlin.apps.cms.viewsets import UserSearchFilterMixin

now = parse("2013-01-01 18:00:00+01:00")


@pytest.fixture
def projects(project_factory, phase_factory):
    project_old = project_factory(name="old")
    project_active = project_factory(name="active")

    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)
    next_week = now + timezone.timedelta(days=7)

    # past phase
    phase_factory(
        start_date=last_week,
        end_date=yesterday,
        module__project=project_old,
    )

    # active phase
    phase_factory(
        start_date=yesterday,
        end_date=next_week,
        module__project=project_active,
    )

    return [project_old, project_active]


@pytest.mark.django_db
def test_form_valid_without_filters(projects):
    form = UserSearchFilterMixin(data={})
    assert form.is_valid()
    with freeze_time(now):
        assert form.filter(Project.objects.all()).count() == 1
        assert form.filter(Project.objects.all()).first().name == "active"


@pytest.mark.django_db
def test_form_filters_past_projects(projects):
    form = UserSearchFilterMixin(data={"show_past": "on"})
    assert form.is_valid()

    with freeze_time(now):
        objects = Project.objects.all()
    filtered = form.filter(objects)

    assert len(filtered) == 2


@pytest.mark.django_db
def test_form_filters_search(projects):
    form = UserSearchFilterMixin(data={"q": "active", "show_past": "on"})
    assert form.is_valid()

    with freeze_time(now):
        objects = Project.objects.all()
    filtered = form.filter(objects)

    assert len(filtered) == 1
    assert filtered.first().name == "active"
