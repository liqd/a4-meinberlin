from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from meinberlin.apps.kiezradar.models import get_search_profiles_for_project
from meinberlin.apps.notifications import emails
from meinberlin.apps.notifications.models import Notification


@shared_task(name="periodic_notifications_cleanup")
def periodic_notifications_cleanup():
    """
    This task makes sure that any notification data older >6 months is deleted.
    """
    Notification.objects.filter(
        action__timestamp__gt=timezone.now() - timedelta(days=180)
    ).delete()


@shared_task
def send_action_notifications(action_pk):
    action = Action.objects.get(pk=action_pk)
    verb = Verbs(action.verb)
    search_profiles = None

    if action.type in ("item", "comment") and verb in (Verbs.CREATE, Verbs.ADD):
        emails.NotifyCreatorEmail.send(action)

        if action.project:
            emails.NotifyModeratorsEmail.send(action)

    elif action.type == "phase" and action.project.project_type == "a4projects.Project":
        if verb == Verbs.START:
            emails.NotifyFollowersOnPhaseStartedEmail.send(action)
        elif verb == Verbs.SCHEDULE:
            emails.NotifyFollowersOnPhaseIsOverSoonEmail.send(action)

    elif action.type == "offlineevent" and verb == Verbs.START:
        emails.NotifyFollowersOnUpcomingEventEmail.send(action)

    elif action.type == "project" and verb == Verbs.PUBLISH:
        search_profiles = get_search_profiles_for_project(action.project)
        for profile in search_profiles:
            emails.NotifyUserOnSearchProfileMatch.send(
                profile, project_pk=action.project.pk
            )

    if Notification.should_notify(action):
        Notification.objects.create_from_action(action, search_profiles)
