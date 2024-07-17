from datetime import datetime
from datetime import timedelta

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

from adhocracy4.phases.models import Phase
from meinberlin.apps import logger
from meinberlin.apps.projects.api import get_public_projects
from meinberlin.apps.projects.serializers import ActiveProjectSerializer
from meinberlin.apps.projects.serializers import FutureProjectSerializer
from meinberlin.apps.projects.serializers import PastProjectSerializer
from meinberlin.apps.projects.serializers import ProjectSerializer


@shared_task(name="set_cache_for_projects")
def set_cache_for_projects() -> str:
    """Sets the cache for all public projects.
    The task is called inline from reset_cache_for_projects,
    whenever there are new future or past projects,
    and also it is scheduled via celery beat to run
    every hour in settings/production.txt.

    Returns:
        A log meesage indicating if cache for
        projects was added succesfully or an error.
    """
    try:
        queryset = get_public_projects()
        now = timezone.now()

        active_projects = queryset.filter(
            module__phase__start_date__lte=now,
            module__phase__end_date__gt=now,
            module__is_draft=False,
        ).distinct()
        data = ActiveProjectSerializer(active_projects, now=now, many=True).data
        cache.set("projects_" + "activeParticipation", data)

        future_projects = (
            queryset.filter(module__phase__start_date__gt=now, module__is_draft=False)
            .distinct()
            .exclude(id__in=active_projects.values("id"))
        )
        data = FutureProjectSerializer(future_projects, now=now, many=True).data
        cache.set("projects_" + "futureParticipation", data)

        past_projects = (
            queryset.filter(module__phase__end_date__lt=now, module__is_draft=False)
            .distinct()
            .exclude(id__in=active_projects.values("id"))
            .exclude(id__in=future_projects.values("id"))
        )
        data = PastProjectSerializer(past_projects, now=now, many=True).data
        cache.set("projects_" + "pastParticipation", data)

        projects = active_projects.union(future_projects, past_projects)
        data = ProjectSerializer(projects, now=now, many=True).data
        cache.set("projects_", data)

        return logger.info("Reset cache for public projects.")

    except Exception as e:
        logger.error("Cache for projects failed:", e)


def get_next_projects_start() -> list:
    """
    Helper function to query the db and retrieve the
    phases for projects that will start in the next 10min.

    Returns:
        A list with the phases timestamp and remaining seconds.
    """
    now = datetime.now(tz=timezone.utc)  # tz is UTC
    phases = (
        Phase.objects.filter(
            module__is_draft=False,
            start_date__isnull=False,
            start_date__range=[now, now + timedelta(minutes=10)],
        )
        .order_by("start_date")
        .all()
    )
    list_format_phases = []
    if phases:
        for phase in phases:
            # compare now with next start date
            phase_start_date = phase.start_date.astimezone(timezone.utc)
            remain_time = phase_start_date - now
            str_phase = phase_start_date.strftime("%Y-%m-%d, %H:%M:%S %Z")
            list_format_phases.append(
                (str_phase, remain_time.total_seconds(), "future")
            )

        # set the redis key: value
        cache.set("next_projects_start", list_format_phases)

    return list_format_phases


def get_next_projects_end() -> list:
    """
    Helper function to query the db and
    retrieve the earliest phase that will end.

    Returns:
        A list with the phases timestamp and remaining seconds.
    """
    now = datetime.now(tz=timezone.utc)  # tz is UTC
    phases = (
        Phase.objects.filter(
            module__is_draft=False,
            end_date__isnull=False,
            end_date__range=[now, now + timedelta(minutes=10)],
        )
        .order_by("end_date")
        .all()
    )

    list_format_phases = []
    if phases:
        for phase in phases:
            # compare now with next start date
            phase_end_date = phase.end_date.astimezone(timezone.utc)
            remain_time = phase_end_date - now
            str_phase = phase_end_date.strftime("%Y-%m-%d, %H:%M:%S %Z")
            list_format_phases.append(
                (str_phase, remain_time.total_seconds(), "active")
            )

        # set the redis key: value
        cache.set("next_projects_end", list_format_phases)

    return list_format_phases


@shared_task(name="schedule_reset_cache_for_projects")
def schedule_reset_cache_for_projects() -> bool:
    """The task is set via celery beat every 10 minutes in
    settings/production.txt.

    Returns:
        A boolean indicating if there are projects
        becoming past or active in the next 10 minutes
        and when the cache will be cleared.

        Task propagates a log info with a list
        of the phases timestamps.
    """

    msg = "Projects will be removed from cache: "
    success = False
    starts = False
    ends = False

    # check if redis has cache for past projects ending
    list_projects_end = cache.get("next_projects_end")
    if not list_projects_end:
        list_projects_end = get_next_projects_end()

    # check if redis has cache for future projects starting
    list_projects_start = cache.get("next_projects_start")
    if not list_projects_start:
        list_projects_start = get_next_projects_start()

    list_timestamps = list_projects_end + list_projects_start

    if list_timestamps:
        for timestamp in list_timestamps:
            project_phase = timestamp[0]
            remain_time = timestamp[1]
            project_status = timestamp[2]
            if project_status == "future":
                starts = True
            else:
                ends = True
            # schedule cache clear for the seconds between now and next end
            reset_cache_for_projects.apply_async([starts, ends], countdown=remain_time)
            msg = f"""
                    {project_status} {project_phase} in {remain_time/60} minutes
                    """
        success = True
    else:
        msg += "None"

    logger.info(msg)
    return success


@shared_task
def reset_cache_for_projects(starts: bool, ends: bool):
    """
    Task called by schedule_reset_cache_for_projects
    and resets cache for projects.
    """
    if starts:
        # remove redis key next_project_start
        cache.delete("next_projects_start")
    if ends:
        # remove redis key next_projects_end
        cache.delete("next_projects_end")

    set_cache_for_projects()
