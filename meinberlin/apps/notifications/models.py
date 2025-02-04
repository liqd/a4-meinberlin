from django.db import models

from adhocracy4.actions.verbs import Verbs
from meinberlin.apps.users.models import User

NOTIFIABLES = (
    "item",
    "comment",
    "rating",
    "moderatorremark",
)


class Notification(models.Model):
    recipient = models.ForeignKey(
        "meinberlin_users.User", on_delete=models.CASCADE, related_name="notifications"
    )
    action = models.ForeignKey(
        "a4actions.action", on_delete=models.CASCADE, related_name="+"
    )
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.recipient} regarding {self.action}"

    @classmethod
    def should_notify(cls, action):
        verb = Verbs(action.verb)
        # if there is someone to notify
        if hasattr(action.target, "creator"):
            if action.type in NOTIFIABLES and verb in (Verbs.CREATE, Verbs.ADD):
                return True, [action.target.creator]

        followers = User.objects.filter(
            follow__project=action.project,
            follow__enabled=True,
        )
        if (
            action.type == "phase"
            and action.project.project_type == "a4projects.Project"
        ):
            if verb == Verbs.START or verb == Verbs.SCHEDULE:
                return True, followers
        elif action.type == "offlineevent" and verb == Verbs.START:
            return True, followers
        return False, []


class NotificationSettings(models.Model):
    email_fields = [
        "email_newsletter",
        "notify_followers_phase_started",
        "notify_followers_phase_over_soon",
        "notify_followers_event_upcoming",
        "notify_creator",
        "notify_creator_on_moderator_feedback",
        "notify_initiators_project_created",
        "notify_moderator",
    ]
    user = models.OneToOneField(
        "meinberlin_users.User",
        on_delete=models.CASCADE,
        related_name="notification_settings",
    )
    email_newsletter = models.BooleanField(default=False)

    """
    Notification fields are being used to check if a notification should be sent
    via email.
    """
    notify_followers_phase_started = models.BooleanField(default=True)
    notify_followers_phase_over_soon = models.BooleanField(default=True)
    notify_followers_event_upcoming = models.BooleanField(default=True)
    notify_creator = models.BooleanField(default=True)
    notify_creator_on_moderator_feedback = models.BooleanField(default=True)
    notify_initiators_project_created = models.BooleanField(default=True)
    notify_moderator = models.BooleanField(default=True)

    """
    Tracked fields are being used to check if a notification should show in
    the activity feed.
    """
    track_followers_phase_started = models.BooleanField(default=True)
    track_followers_phase_over_soon = models.BooleanField(default=True)
    track_followers_event_upcoming = models.BooleanField(default=True)

    def update_all_settings(self, notifications_on, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.BooleanField):
                if field.name in kwargs:
                    setattr(self, field.name, kwargs[field.name])
                else:
                    setattr(self, field.name, notifications_on)
        self.save()

    def update_email_settings(self, notifications_on, **kwargs):
        for field in self.email_fields:
            if field in kwargs:
                setattr(self, field, kwargs[field])
            else:
                setattr(self, field, notifications_on)
        self.save()
