import factory
from django.db.models.signals import post_save

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.notifications.models import NotificationSettings


@factory.django.mute_signals(post_save)
class NotificationSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NotificationSettings

    user = factory.SubFactory(a4_factories.USER_FACTORY)
    email_newsletter = False
    notify_followers_phase_started = True
    notify_followers_phase_over_soon = True
    notify_followers_event_upcoming = True
    notify_creator = True
    notify_creator_on_moderator_feedback = True
    notify_initiators_project_created = True
    notify_moderator = True
    track_followers_phase_started = True
    track_followers_phase_over_soon = True
    track_followers_event_upcoming = True
