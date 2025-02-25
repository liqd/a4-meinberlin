from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from adhocracy4.comments.models import Comment
from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.phases.models import Phase
from adhocracy4.polls.models import Answer
from adhocracy4.polls.models import Vote
from adhocracy4.polls.signals import poll_voted
from adhocracy4.projects.models import Project
from adhocracy4.ratings.models import Rating
from meinberlin.apps.budgeting.models import Proposal
from meinberlin.apps.ideas.models import Idea
from meinberlin.apps.likes.models import Like
from meinberlin.apps.livequestions.models import LiveQuestion
from meinberlin.apps.mapideas.models import MapIdea
from meinberlin.apps.projects.models import ProjectInsight
from meinberlin.apps.projects.tasks import set_cache_for_projects
from meinberlin.apps.topicprio.models import Topic


@receiver(a4dashboard_signals.project_created)
@receiver(a4dashboard_signals.project_published)
@receiver(a4dashboard_signals.project_unpublished)
@receiver(a4dashboard_signals.project_component_updated)
def post_dashboard_signal_delete(sender, project, user, **kwargs):
    """Refresh project, plan and extproject cache on dashboard signal"""
    set_cache_for_projects.delay_on_commit(get_next_projects=True)


@receiver(a4dashboard_signals.module_published)
@receiver(a4dashboard_signals.module_unpublished)
def post_module_publish_unpublish(sender, module, **kwargs):
    """Refresh project, plan and extproject cache on module (un)publish"""
    set_cache_for_projects.delay_on_commit(get_next_projects=True)


@receiver(post_save, sender=Phase)
@receiver(post_delete, sender=Phase)
def post_phase_save_delete(sender, instance, **kwargs):
    """Refresh project, plan and extproject cache on phase save or delete"""
    set_cache_for_projects.delay_on_commit(get_next_projects=True)


@receiver(post_delete, sender=Project)
def post_save_delete(sender, instance, *args, **kwargs):
    """
    Refresh cache for project list views.
    Capture any new phases that may got created/updated while saving a project.
    """
    set_cache_for_projects.delay_on_commit(
        projects=True, get_next_projects=True, ext_projects=False, plans=False
    )


@receiver(post_save, sender=Comment)
def increase_comments_count(sender, instance, created, **kwargs):
    if created and instance.project:
        insight, _ = ProjectInsight.objects.get_or_create(project=instance.project)
        insight.comments += 1
        insight.save()
        insight.active_participants.add(instance.creator.id)


@receiver(post_save, sender=Idea)
@receiver(post_save, sender=MapIdea)
@receiver(post_save, sender=Proposal)
@receiver(post_save, sender=Topic)
def increase_idea_count(sender, instance, created, **kwargs):
    if not created:
        return

    insight, _ = ProjectInsight.objects.get_or_create(project=instance.module.project)
    insight.written_ideas += 1
    insight.save()

    if sender != Topic:
        insight.active_participants.add(instance.creator.id)


@receiver(post_save, sender=Rating)
def increase_rating_count(sender, instance, created, **kwargs):
    insight, _ = ProjectInsight.objects.get_or_create(project=instance.module.project)
    if created:
        insight.ratings += 1
        insight.active_participants.add(instance.creator.id)
        insight.save()
    if instance.value == 0:
        insight.ratings -= 1
        insight.active_participants.remove(instance.creator.id)
        insight.save()


@receiver(post_save, sender=LiveQuestion)
def increase_live_questions_count(sender, instance, created, **kwargs):
    if created:
        project = instance.module.project
        insight, _ = ProjectInsight.objects.get_or_create(project=project)
        insight.live_questions += 1
        insight.save()


@receiver(post_save, sender=Like)
def increase_ratings_count_for_likes(sender, instance, created, **kwargs):
    if created:
        project = instance.question.module.project
        insight, _ = ProjectInsight.objects.get_or_create(project=project)
        insight.ratings += 1
        insight.save()


@receiver(post_save, sender=Vote)
@receiver(post_save, sender=Answer)
def increase_poll_answers_count(sender, instance, created, **kwargs):
    if created:
        if sender == Answer:
            project = instance.question.poll.module.project
        else:
            project = instance.project

        insight, _ = ProjectInsight.objects.get_or_create(project=project)
        insight.poll_answers += 1
        insight.save()


@receiver(poll_voted)
def increase_poll_participant_count(sender, poll, creator, content_id, **kwargs):
    insight, _ = ProjectInsight.objects.get_or_create(project=poll.module.project)
    if creator:
        insight.active_participants.add(creator.id)
    else:
        insight.unregistered_participants += 1
    insight.save()
