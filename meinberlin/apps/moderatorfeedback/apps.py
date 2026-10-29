from django.apps import AppConfig


def _notify_creator_on_feedback(sender, item, user, **kwargs):
    from meinberlin.apps.notifications.emails import (
        NotifyCreatorOrContactOnModeratorFeedback,
    )

    NotifyCreatorOrContactOnModeratorFeedback.send(item)


class Config(AppConfig):
    name = "meinberlin.apps.moderatorfeedback"
    label = "meinberlin_moderatorfeedback"

    def ready(self):
        from adhocracy4.moderation.signals import moderation_item_feedback_saved

        moderation_item_feedback_saved.connect(
            _notify_creator_on_feedback,
            dispatch_uid="meinberlin_moderatorfeedback_notify_creator",
        )
