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


# @shared_task
# def send_action_notifications(action_pk):
#     action = Action.objects.get(pk=action_pk)
#     verb = Verbs(action.verb)
#     search_profiles = None

#     if action.type in ("item", "comment") and verb in (Verbs.CREATE, Verbs.ADD):
#         emails.NotifyCreatorEmail.send(action)

#         if action.project:
#             emails.NotifyModeratorsEmail.send(action)

#     elif (
#         action.type == "phase"
#         and action.project
#         and action.project.project_type == "a4projects.Project"
#     ):
#         is_offline_event = (
#             hasattr(action.obj, "type")
#             and action.obj.type
#             and action.obj.type.contains("offline-event")
#         )

#         if verb == Verbs.START:
#             if is_offline_event:
#                 pass  # dont actually want emails when offline event is starting
#                 # from meinberlin.apps.offlineevents.models import OfflineEventItem
#                 # event = OfflineEventItem.objects.filter(module=action.obj.module).first()
#                 # if event:
#                 #     emails.NotifyFollowersOnUpcomingEventEmail.send(action, event_id=event.id)
#                 # else:
#                 #     emails.NotifyFollowersOnUpcomingEventEmail.send(action)
#             else:
#                 emails.NotifyFollowersOnPhaseStartedEmail.send(action)

#         elif verb == Verbs.SCHEDULE:
#             if is_offline_event:
#                 from meinberlin.apps.offlineevents.models import OfflineEventItem

#                 event = OfflineEventItem.objects.filter(
#                     module=action.obj.module
#                 ).first()
#                 if event:
#                     emails.NotifyFollowersOnUpcomingEventEmail.send(
#                         action, event_id=event.id
#                     )
#                 else:
#                     emails.NotifyFollowersOnUpcomingEventEmail.send(action)
#             else:
#                 emails.NotifyFollowersOnPhaseIsOverSoonEmail.send(action)

#     # Deprecated - kept for backward compatibility
#     elif action.type == "offlineevent" and verb == Verbs.START:
#         emails.NotifyFollowersOnUpcomingEventEmail.send(action)

#     elif action.type in ("project", "plan") and verb == Verbs.PUBLISH:
#         search_profiles = handle_publish_emails(action)

#     if Notification.should_notify(action):
#         Notification.objects.create_from_action(action, search_profiles)


# @shared_task
# def send_action_notifications(action_pk):
#     action = Action.objects.get(pk=action_pk)
#     verb = Verbs(action.verb)
#     search_profiles = None

#     print("heyyyyyyyyyy")

#     if action.type in ("item", "comment") and verb in (Verbs.CREATE, Verbs.ADD):
#         emails.NotifyCreatorEmail.send(action)

#         if action.project:
#             emails.NotifyModeratorsEmail.send(action)

#     elif action.type == "phase" and action.project.project_type == "a4projects.Project":
#         is_offline_event = hasattr(action.obj, "type") and action.obj.type.endswith(
#             "offline-event"
#         )

#         if verb == Verbs.SCHEDULE and is_offline_event:
#             # Get the actual OfflineEventItem from the module
#             event = OfflineEventItem.objects.filter(module=action.obj.module).first()

#         # if verb == Verbs.START:
#         #     if is_offline_event:
#         #         # This might have been in place before but don't think it's desired
#         #         pass
#         #     #     # Offline event starting now - send upcoming event email
#         #     #     emails.NotifyFollowersOnUpcomingEventEmail.send(action)
#         #     else:
#         #         emails.NotifyFollowersOnPhaseStartedEmail.send(action)

#         if verb == Verbs.START:
#             print(f"START verb - phase type: {getattr(action.obj, 'type', 'No type')}")
#             print(f"is_offline_event: {is_offline_event}")
#             print(f"Action type: {action.type}")
#             print(f"Project exists: {action.project is not None}")

#             if is_offline_event:
#                 print("DEBUG: Skipping offline event START")
#                 pass
#             else:
#                 print("DEBUG: Sending phase started email")
#                 emails.NotifyFollowersOnPhaseStartedEmail.send(action)
#                 print("DEBUG: Email sent")

#         elif verb == Verbs.SCHEDULE:
#             if is_offline_event:
#                 # Offline event happening soon - send upcoming event email
#                 # This matches the old 72-hour notification behavior
#                 event = OfflineEventItem.objects.filter(
#                     module=action.obj.module
#                 ).first()
#                 emails.NotifyFollowersOnUpcomingEventEmail.send(action)
#             else:
#                 emails.NotifyFollowersOnPhaseIsOverSoonEmail.send(action)

#     # Deprecated
#     elif action.type == "offlineevent" and verb == Verbs.START:
#         emails.NotifyFollowersOnUpcomingEventEmail.send(action)

#     elif action.type in ("project", "plan") and verb == Verbs.PUBLISH:
#         search_profiles = handle_publish_emails(action)

#     if Notification.should_notify(action):
#         Notification.objects.create_from_action(action, search_profiles)


@shared_task
def send_action_notifications(action_pk):
    import sys
    import traceback

    try:
        sys.stderr.write(f"\n🔵 TASK STARTED: action_pk={action_pk}\n")
        sys.stderr.flush()

        action = Action.objects.get(pk=action_pk)
        sys.stderr.write(
            f"🔵 Action loaded: id={action.id}, type={action.type}, verb={action.verb}\n"
        )

        # Check project
        if action.project:
            sys.stderr.write(
                f"🔵 Project: id={action.project.id}, type={action.project.project_type}\n"
            )
        else:
            sys.stderr.write(f"🔵 No project!\n")
            return

        # Check object
        if action.obj:
            sys.stderr.write(
                f"🔵 Object: type={type(action.obj)}, has_type={hasattr(action.obj, 'type')}\n"
            )
            if hasattr(action.obj, "type"):
                sys.stderr.write(f"🔵 Object.type={action.obj.type}\n")
        else:
            sys.stderr.write(f"🔵 No obj!\n")

        verb = Verbs(action.verb)
        sys.stderr.write(f"🔵 Verb enum: {verb.value}\n")

        search_profiles = None

        if action.type in ("item", "comment") and verb in (Verbs.CREATE, Verbs.ADD):
            sys.stderr.write(f"🔵 Item/comment notification\n")
            emails.NotifyCreatorEmail.send(action)

            if action.project:
                emails.NotifyModeratorsEmail.send(action)

        elif (
            action.type == "phase"
            and action.project
            and action.project.project_type == "a4projects.Project"
        ):
            sys.stderr.write(f"🔵 Entered phase block\n")

            is_offline_event = (
                hasattr(action.obj, "type")
                and action.obj.type
                and action.obj.type.endswith("offline-event")
            )

            sys.stderr.write(f"🔵 is_offline_event: {is_offline_event}\n")

            if verb == Verbs.START:
                sys.stderr.write(f"🔵 In START branch\n")
                if is_offline_event:
                    sys.stderr.write(f"🔵 Skipping offline event START\n")
                    pass
                else:
                    sys.stderr.write(f"🔵 ABOUT TO SEND PHASE STARTED EMAIL\n")
                    emails.NotifyFollowersOnPhaseStartedEmail.send(action)
                    sys.stderr.write(f"🔵 EMAIL SEND CALLED for phase started\n")

            elif verb == Verbs.SCHEDULE:
                sys.stderr.write(f"🔵 In SCHEDULE branch\n")
                if is_offline_event:
                    sys.stderr.write(
                        f"🔍 SCHEDULE verb on offline event - fetching event for email\n"
                    )
                    from meinberlin.apps.offlineevents.models import OfflineEventItem

                    event = OfflineEventItem.objects.filter(
                        module=action.obj.module
                    ).first()
                    if event:
                        sys.stderr.write(
                            f"✅ Found event: {event.name} (ID: {event.id})\n"
                        )
                        sys.stderr.write(f"   Event date: {event.event_date}\n")
                        emails.NotifyFollowersOnUpcomingEventEmail.send(
                            action, event_id=event.id
                        )
                        sys.stderr.write(f"🔵 EMAIL SEND CALLED for upcoming event\n")
                    else:
                        sys.stderr.write(f"❌ No event found for module!\n")
                        emails.NotifyFollowersOnUpcomingEventEmail.send(action)
                        sys.stderr.write(
                            f"🔵 EMAIL SEND CALLED for upcoming event (fallback)\n"
                        )
                else:
                    sys.stderr.write(f"📧 Sending phase ends soon email\n")
                    emails.NotifyFollowersOnPhaseIsOverSoonEmail.send(action)
                    sys.stderr.write(f"🔵 EMAIL SEND CALLED for phase ends soon\n")

        # Deprecated - kept for backward compatibility
        elif action.type == "offlineevent" and verb == Verbs.START:
            sys.stderr.write(f"⚠️ Deprecated offlineevent action type detected\n")
            emails.NotifyFollowersOnUpcomingEventEmail.send(action)

        elif action.type in ("project", "plan") and verb == Verbs.PUBLISH:
            sys.stderr.write(f"📧 Publishing {action.type}\n")
            search_profiles = handle_publish_emails(action)

        # Create notifications if needed
        if Notification.should_notify(action):
            sys.stderr.write(f"🔔 Creating notification for action {action_pk}\n")
            Notification.objects.create_from_action(action, search_profiles)

        sys.stderr.write(f"🔵 TASK COMPLETED SUCCESSFULLY for action {action_pk}\n")
        sys.stderr.flush()

    except Exception as e:
        sys.stderr.write(f"🔴 EXCEPTION IN TASK: {e}\n")
        sys.stderr.write(traceback.format_exc())
        sys.stderr.flush()
        raise  # Re-raise so Celery knows it failed


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
