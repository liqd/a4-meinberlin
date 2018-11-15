from django.core.management.base import BaseCommand
from django.utils import timezone

from adhocracy4.projects.models import Project


class Command(BaseCommand):

    def handle(self, *args, **options):

        for project in Project.objects.all():
            if project.active_phase:
                phase = project.active_phase
                now = timezone.now()
                if phase.start_date and phase.start_date < now:
                    time = project.active_phase.end_date
                    time_delta = time - now
                    days = time_delta.days
                    relevance = round(1 / days, 2)
                    project.relevance = relevance
            else:
                project.relevance = 0
            project.save()
