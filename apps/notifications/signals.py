from django.db.models import signals
from django.dispatch import receiver

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.follows.models import Follow
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project

from . import emails


@receiver(signals.post_save, sender=Action)
def send_notifications(instance, created, **kwargs):
    action = instance
    verb = Verbs(action.verb)

    if verb == Verbs.CREATE or verb == Verbs.ADD:
        emails.NotifyCreatorEmail.send(action)

        if action.project:
            emails.NotifyModeratorsEmail.send(action)
            emails.NotifyFollowersOnNewItemCreated.send(action)

    elif verb == Verbs.SCHEDULE:
        if isinstance(action.obj, Phase):
            emails.NotifyFollowersOnPhaseIsOverSoonEmail.send(action)


@receiver(signals.m2m_changed, sender=Project.moderators.through)
def autofollow_project_moderators(instance, action, pk_set, reverse, **kwargs):
    if action == 'post_add':
        if not reverse:
            project = instance
            users_pks = pk_set

            for user_pk in users_pks:
                Follow.objects.update_or_create(
                    project=project,
                    creator_id=user_pk,
                    defaults={
                        'enabled': True
                    }
                )
        else:
            user = instance
            project_pks = pk_set

            for project_pk in project_pks:
                Follow.objects.update_or_create(
                    project_id=project_pk,
                    creator_id=user,
                    defaults={
                        'enabled': True
                    }
                )
