from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils import timezone

from adhocracy4.projects.models import Project
from meinberlin.apps.projects.utils import apply_publish_results_reminder
from meinberlin.apps.projects.utils import get_publish_results_reminder_skip_reason


class Command(BaseCommand):
    help = (
        "Send the publish-results reminder email to every initiator of the project's "
        "organisation (one message per initiator), only if the project satisfies the "
        "same eligibility rules as the periodic send_publish_results_reminders task."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "project_slug",
            help="Project slug as in /projekte/<slug>/",
        )

    def handle(self, *args, **options):
        slug = options["project_slug"]
        try:
            project = (
                Project.objects.select_related("organisation", "insight")
                .prefetch_related(
                    "module_set",
                    "module_set__phase_set",
                    "organisation__initiators__notification_settings",
                )
                .get(slug=slug)
            )
        except Project.DoesNotExist as exc:
            raise CommandError(f'No project with slug "{slug}".') from exc

        now = timezone.now()
        reason = get_publish_results_reminder_skip_reason(project, now=now)
        if reason is not None:
            raise CommandError(
                f'Project "{slug}" does not qualify for a publish-results reminder '
                f"(same rules as the periodic task). Reason code: {reason}."
            )

        n_initiators = project.organisation.initiators.count()
        apply_publish_results_reminder(project, now=now)
        self.stdout.write(
            self.style.SUCCESS(
                f"Publish-results reminder sent for project {slug!r}: "
                f"{n_initiators} e-mail(s), one per initiator of the organisation."
            )
        )
