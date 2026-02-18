# flake8: noqa
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from meinberlin.apps.kiezradar.matchers import get_search_profiles_for_obj
from meinberlin.apps.notifications import emails
from meinberlin.apps.notifications.models import Notification
from meinberlin.apps.offlineevents.models import OfflineEventItem


@shared_task(name="periodic_notifications_cleanup")
def periodic_notifications_cleanup():
    """
    This task makes sure that any notification data older >6 months is deleted.
    """
    Notification.objects.filter(
        action__timestamp__lt=timezone.now() - timedelta(days=180)
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

    elif (
        action.type == "phase"
        and action.project
        and action.project.project_type == "a4projects.Project"
    ):
        is_offline_event = (
            hasattr(action.obj, "type")
            and action.obj.type
            and action.obj.type.endswith("offline-event")
        )

        if verb == Verbs.START:
            if is_offline_event:
                # Offline event starting now - no action needed
                pass
            else:
                emails.NotifyFollowersOnPhaseStartedEmail.send(action)

        elif verb == Verbs.SCHEDULE:
            if is_offline_event:
                from meinberlin.apps.offlineevents.models import OfflineEventItem

                event = OfflineEventItem.objects.filter(
                    module=action.obj.module
                ).first()
                if event:
                    emails.NotifyFollowersOnUpcomingEventEmail.send(
                        action, event_id=event.id
                    )
                else:
                    emails.NotifyFollowersOnUpcomingEventEmail.send(action)
            else:
                emails.NotifyFollowersOnPhaseIsOverSoonEmail.send(action)

    # Deprecated - kept for backward compatibility
    elif action.type == "offlineevent" and verb == Verbs.START:
        emails.NotifyFollowersOnUpcomingEventEmail.send(action)

    elif action.type in ("project", "plan") and verb == Verbs.PUBLISH:
        search_profiles = handle_publish_emails(action)

    if Notification.should_notify(action):
        Notification.objects.create_from_action(action, search_profiles)


def handle_publish_emails(action):
    if action.type == "project":
        search_profiles = get_search_profiles_for_obj(action.project)
    else:
        search_profiles = get_search_profiles_for_obj(action.obj)

    for profile in search_profiles:
        emails.NotifyUserOnSearchProfileMatch.send(
            profile,
            action_pk=action.pk,
        )
    return search_profiles
