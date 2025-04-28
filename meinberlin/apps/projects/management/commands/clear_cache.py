from django.core.cache import cache
from django.core.management.base import BaseCommand

from meinberlin.apps import logger


class Command(BaseCommand):
    help = "Clear the cache for projects and plans"

    def handle(self, *args, **options):
        active_projects = cache.delete("projects_activeParticipation")
        future_projects = cache.delete("projects_futureParticipation")
        past_projects = cache.delete("projects_pastParticipation")
        extprojects = cache.delete("extprojects")
        projects = cache.delete("projects_")
        plans = cache.delete("plans")

        logger.info(
            f"""cleared cache for
            active_projects: {active_projects},
            future_projects: {future_projects},
            past_projects: {past_projects},
            projects: {projects},
            extprojects: {extprojects},
            plans: {plans}.
            """
        )
