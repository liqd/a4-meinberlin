from dataclasses import dataclass
from typing import List
from unittest.mock import Mock

import pytest
from django.utils import timezone

from meinberlin.apps.projects.filters import StatusFilter
from meinberlin.apps.projects.models import Project


@dataclass
class TestCase:
    """
    A `TestCase` is a helper for writing status filter tests. It contains all the data necessary for creating the
    projects, modules and phases required for a single test scenario. Time is treated in discrete steps with values
    between 0 and 9 (they correspond to hours of a single day).

    The dictionary `projects` is a tree with two levels, one for the modules of a project and one for the phases
    of a module. Each leaf node consists of two integers: the start and the end time index of a single phase. The keys
    are `"modules"` for the first level and `"phases"` for the second and each value must be a list.

    Example A: 1 project, 1 module, 1 phase that starts at time 3 and finishes at time 5
        projects = [dict(modules=[dict(phases=[(3, 5)])])]

    Example B: 1 project, 2 modules, each 1 phase that starts at time 1 and finishes at time 3
        projects = [dict(modules=[dict(phases=[(1, 3)]), dict(phases=[(1, 3)])])]

    The `n_{past,active,future}_expected` fields define how many projects we expect to find in each category after
    the status filter has been applied.
    """

    now: int
    projects: List[dict]
    n_past_expected: int = 0
    n_active_expected: int = 0
    n_future_expected: int = 0


def get_failing_edge_cases() -> List[TestCase]:
    return [
        TestCase(
            now=1, projects=[dict(modules=[dict(phases=[(0, 1)])])], n_past_expected=1
        ),
    ]


def get_test_cases() -> List[TestCase]:
    test_cases = [
        TestCase(
            now=2, projects=[dict(modules=[dict(phases=[(0, 1)])])], n_past_expected=1
        ),
        TestCase(
            now=1, projects=[dict(modules=[dict(phases=[(0, 2)])])], n_active_expected=1
        ),
        TestCase(
            now=0, projects=[dict(modules=[dict(phases=[(0, 1)])])], n_active_expected=1
        ),
        TestCase(
            now=3,
            projects=[dict(modules=[dict(phases=[(1, 2), (4, 5), (1, 5)])])],
            n_active_expected=1,
        ),
        TestCase(
            now=0, projects=[dict(modules=[dict(phases=[(1, 2)])])], n_future_expected=1
        ),
        TestCase(
            now=3,
            projects=[dict(modules=[dict(phases=[(1, 2), (4, 5)])])],
            n_future_expected=1,
        ),
    ]

    return test_cases


@pytest.mark.django_db
@pytest.mark.parametrize("test_case", get_test_cases())
def test_status_filter(
    project_factory, module_factory, phase_factory, test_case: TestCase
):
    time = [timezone.datetime(2023, 1, 1, i, 0, 0, 0) for i in range(10)]
    now = time[test_case.now]
    request = Mock()
    view = Mock()
    view.now = now

    for project_data in test_case.projects:
        project = project_factory()
        project.save()

        for module_data in project_data["modules"]:
            module = module_factory(project=project)

            for start, end in module_data["phases"]:
                phase_factory(module=module, start_date=time[start], end_date=time[end])

    status_filter = StatusFilter()

    request.GET = {"status": "activeParticipation"}
    n_active_project = status_filter.filter_queryset(
        request=request, queryset=Project.objects.all(), view=view
    ).count()

    request.GET = {"status": "pastParticipation"}
    n_past_project = status_filter.filter_queryset(
        request=request, queryset=Project.objects.all(), view=view
    ).count()

    request.GET = {"status": "futureParticipation"}
    n_future_project = status_filter.filter_queryset(
        request=request, queryset=Project.objects.all(), view=view
    ).count()

    assert n_active_project == test_case.n_active_expected
    assert n_past_project == test_case.n_past_expected
    assert n_future_project == test_case.n_future_expected
