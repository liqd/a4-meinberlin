from django.db.models import Q
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver

from adhocracy4.comments.models import Comment
from adhocracy4.dashboard import signals as a4dashboard_signals
from adhocracy4.modules.models import Item
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


def is_contributor(project, creator):
    return (
        Item.objects.filter(
            creator=creator, module__in=project.module_set.all()
        ).exists()
        or Comment.objects.filter(creator=creator, project=project).exists()
        or Vote.objects.filter(
            choice__question__poll__module__project=project, creator=creator
        ).exists()
        or Answer.objects.filter(
            question__poll__module__project=project, creator=creator
        ).exists()
        or Rating.objects.filter(
            Q(idea__module__project=project)
            | Q(topic__module__project=project)
            | Q(mapidea__module__project=project)
            | Q(maptopic__module__project=project)
            | Q(budget_proposal__module__project=project)
            | Q(comment__project=project),
            creator=creator,
        )
        .exclude(value=0)
        .exists()
    )


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


@receiver(post_delete, sender=Comment)
def decrease_comments_count(sender, instance, using, origin, **kwargs):
    """
    Comments are normally not deleted and instead are overwritten,
    but when deleting an item with comments, these comments also get deleted.
    This case covers this.
    """
    if instance.project:
        insight, _ = ProjectInsight.objects.get_or_create(project=instance.project)
        insight.comments = max(0, insight.comments - 1)
        insight.save()

        if not is_contributor(instance.project, instance.creator):
            insight.active_participants.remove(instance.creator)


@receiver(post_save, sender=Idea)
@receiver(post_save, sender=MapIdea)
@receiver(post_save, sender=Proposal)
def increase_idea_count(sender, instance, created, **kwargs):
    if not created:
        return

    insight, _ = ProjectInsight.objects.get_or_create(project=instance.module.project)
    insight.written_ideas += 1
    insight.save()

    insight.active_participants.add(instance.creator.id)


@receiver(pre_delete, sender=Idea)
@receiver(pre_delete, sender=MapIdea)
@receiver(pre_delete, sender=Proposal)
def decrease_idea_count(sender, instance, using, **kwargs):
    # Determine project before deletion, because after delete the relation may no longer resolve
    project = instance.module.project
    insight, _ = ProjectInsight.objects.get_or_create(project=project)
    insight.written_ideas = max(0, insight.written_ideas - 1)
    insight.save()

    if not is_contributor(project, instance.creator):
        insight.active_participants.remove(instance.creator)


@receiver(pre_save, sender=Rating)
def set_old_rating_value(sender, instance, **kwargs):
    """Store the old rating value on the instance before saving, if it exists."""
    if instance.pk:
        old_instance = Rating.objects.get(pk=instance.pk)
        instance._old_value = old_instance.value
    else:
        instance._old_value = None


@receiver(post_save, sender=Rating)
def increase_rating_count(sender, instance, created, **kwargs):
    insight, _ = ProjectInsight.objects.get_or_create(project=instance.module.project)
    if created:
        insight.ratings += 1
        insight.active_participants.add(instance.creator.id)
        insight.save()
        return

    old_val = instance._old_value
    new_val = instance.value

    if old_val == 0 and new_val != 0:
        insight.ratings += 1
        insight.active_participants.add(instance.creator.id)
        insight.save()
    elif old_val != 0 and new_val == 0:
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
            project = instance.module.project

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
