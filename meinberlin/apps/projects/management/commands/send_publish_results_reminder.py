from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from adhocracy4.projects.models import Project
from meinberlin.apps.notifications import emails as notification_emails


class Command(BaseCommand):
    help = (
        "Send the publish-results reminder email to every initiator of the project's "
        "organisation (one message per initiator). Ignores participation end date, "
        "empty results field, and whether a reminder was sent before (unlike the "
        "periodic task). Refuses draft projects unless --force is passed."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "project_slug",
            help="Project slug as in /projekte/<slug>/",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Send even if the project is still a draft (not published).",
        )

    def handle(self, *args, **options):
        slug = options["project_slug"]
        force = options["force"]
        try:
            project = Project.objects.select_related("organisation").get(slug=slug)
        except Project.DoesNotExist as exc:
            raise CommandError(f'No project with slug "{slug}".') from exc

        if project.project_type != "a4projects.Project":
            raise CommandError(
                f'Project "{slug}" has type {project.project_type!r}; '
                "this reminder only applies to standard projects (a4projects.Project)."
            )

        if project.is_draft and not force:
            raise CommandError(
                f'Project "{slug}" is still a draft (not published). '
                "Use --force to send anyway, or publish the project first."
            )

        n_initiators = project.organisation.initiators.count()
        notification_emails.NotifyInitiatorsPublishResultsEmail.send(project)
        self.stdout.write(
            self.style.SUCCESS(
                f"Publish-results reminder sent for project {slug!r}: "
                f"{n_initiators} e-mail(s), one per initiator of the organisation."
            )
        )
