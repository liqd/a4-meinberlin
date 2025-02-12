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
