from django.contrib import auth

from adhocracy4.actions.models import Action
from adhocracy4.emails import Email
from meinberlin.apps.extprojects.models import ExternalProject

User = auth.get_user_model()


def _exclude_actor(receivers, actor):
    if not actor:
        return receivers

    if hasattr(receivers, "exclude"):
        return receivers.exclude(id=actor.id)

    return [receiver for receiver in receivers if not receiver == actor]


def _exclude_moderators(receivers, action):
    if hasattr(action, "project"):
        moderator_ids = action.project.moderators.values_list("id", flat=True)

        if hasattr(receivers, "exclude"):
            return receivers.exclude(id__in=moderator_ids)

        return [user for user in receivers if user.id not in moderator_ids]

    return receivers


def _exclude_notifications_disabled(receivers, notification_type):
    if hasattr(receivers, "filter"):
        filters = {f"notification_settings__{notification_type}": True}
        return receivers.filter(**filters)

    return [
        user
        for user in receivers
        if getattr(user.notification_settings, notification_type)
    ]


class NotifyCreatorEmail(Email):
    template_name = "meinberlin_notifications/emails/notify_creator"

    def get_receivers(self):
        action = self.object
        if hasattr(action.target, "creator"):
            receivers = [action.target.creator]
            receivers = _exclude_notifications_disabled(receivers, "notify_creator")
            receivers = _exclude_actor(receivers, action.actor)
            receivers = _exclude_moderators(receivers, action)
            return receivers
        return []


class NotifyCreatorOrContactOnModeratorFeedback(Email):
    template_name = (
        "meinberlin_notifications/emails/notify_creator_on_moderator_feedback"
    )

    def get_receivers(self):
        if hasattr(self.object, "contact_email"):
            #  send to contact
            receivers = [self.object.contact_email]
        else:
            #  send to creator
            receivers = [self.object.creator]
            receivers = _exclude_notifications_disabled(
                receivers, "notify_creator_on_moderator_feedback"
            )
        return receivers

    def get_context(self):
        context = super().get_context()
        context["object"] = self.object
        if not hasattr(self.object, "contact_email"):
            #  send to creator
            context["send_to_creator"] = True
        return context


class NotifyModeratorsEmail(Email):
    template_name = "meinberlin_notifications/emails/notify_moderator"

    def get_receivers(self):
        action = self.object
        receivers = action.project.moderators.all()
        receivers = _exclude_actor(receivers, action.actor)
        receivers = _exclude_notifications_disabled(receivers, "notify_moderator")
        return receivers


class NotifyInitiatorsOnProjectCreatedEmail(Email):
    template_name = "meinberlin_notifications/emails/notify_initiators_project_created"

    def get_receivers(self):
        project = self.object
        creator = User.objects.get(pk=self.kwargs["creator_pk"])
        receivers = project.organisation.initiators.all()
        receivers = _exclude_actor(receivers, creator)
        receivers = _exclude_notifications_disabled(
            receivers, "notify_initiators_project_created"
        )
        return receivers

    def get_context(self):
        context = super().get_context()
        creator = User.objects.get(pk=self.kwargs["creator_pk"])
        context["creator"] = creator
        context["project"] = self.object
        return context


class NotifyFollowersOnPhaseStartedEmail(Email):
    template_name = "meinberlin_notifications/emails/notify_followers_phase_started"

    def get_receivers(self):
        action = self.object
        receivers = User.objects.filter(
            follow__project=action.project,
            follow__enabled=True,
        )
        receivers = _exclude_notifications_disabled(
            receivers, "notify_followers_phase_started"
        )
        return receivers


class NotifyFollowersOnPhaseIsOverSoonEmail(Email):
    template_name = "meinberlin_notifications/emails/notify_followers_phase_over_soon"

    def get_receivers(self):
        action = self.object
        receivers = User.objects.filter(
            follow__project=action.project,
            follow__enabled=True,
        )
        receivers = _exclude_notifications_disabled(
            receivers, "notify_followers_phase_over_soon"
        )
        return receivers


class NotifyFollowersOnUpcomingEventEmail(Email):
    template_name = "meinberlin_notifications/emails/notify_followers_event_upcoming"

    def get_receivers(self):
        action = self.object
        receivers = User.objects.filter(
            follow__project=action.project,
            follow__enabled=True,
        )
        receivers = _exclude_notifications_disabled(
            receivers, "notify_followers_event_upcoming"
        )
        return receivers


class NotifyUserOnSearchProfileMatch(Email):
    template_name = "meinberlin_notifications/emails/notify_new_search_profile_project"

    def get_receivers(self):
        profile = self.object
        return [profile.creator]

    def get_context(self):
        context = super().get_context()
        action = Action.objects.get(pk=self.kwargs["action_pk"])
        context["object"] = self.get_polymorphic_object(action)
        context["is_plan"] = not self.is_project(action)
        return context

    def get_polymorphic_object(self, action):
        if action.type == "project":
            try:
                external_project = ExternalProject.objects.get(pk=action.project.pk)
                return external_project
            except ExternalProject.DoesNotExist:
                return action.project
        return action.obj

    def is_project(self, action):
        return action.type == "project"
