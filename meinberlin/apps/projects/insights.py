from typing import Iterable
from typing import List

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q

from adhocracy4.comments.models import Comment
from adhocracy4.polls.models import Answer
from adhocracy4.polls.models import Poll
from adhocracy4.polls.models import Vote
from adhocracy4.projects.models import Project
from adhocracy4.ratings.models import Rating
from meinberlin.apps.budgeting.models import Proposal
from meinberlin.apps.ideas.models import Idea
from meinberlin.apps.likes.models import Like
from meinberlin.apps.livequestions.models import LiveQuestion
from meinberlin.apps.mapideas.models import MapIdea
from meinberlin.apps.maptopicprio.models import MapTopic
from meinberlin.apps.projects.models import ProjectInsight
from meinberlin.apps.topicprio.models import Topic


def create_insights(projects: Iterable[Project]) -> List[ProjectInsight]:
    return [create_insight(project=project) for project in projects]


def create_insight(project: Project) -> ProjectInsight:
    modules = project.modules.all()

    ideas = Idea.objects.filter(module__in=modules)
    map_ideas = MapIdea.objects.filter(module__in=modules)
    comments = Comment.objects.filter(
        Q(project=project) | Q(parent_comment__project=project)
    )
    proposals = Proposal.objects.filter(module__in=modules)
    polls = Poll.objects.filter(module__in=modules)
    votes = Vote.objects.filter(choice__question__poll__in=polls)
    answers = Answer.objects.filter(question__poll__in=polls)
    live_questions = LiveQuestion.objects.filter(module__in=modules)
    likes = Like.objects.filter(question__in=live_questions)
    topics = Topic.objects.filter(module__in=modules)
    map_topics = MapTopic.objects.filter(module__in=modules)

    values = [Rating.POSITIVE, Rating.NEGATIVE]
    ratings_ideas = Rating.objects.filter(idea__in=ideas, value__in=values)
    ratings_map_ideas = Rating.objects.filter(mapidea__in=map_ideas, value__in=values)
    ratings_comments = Rating.objects.filter(comment__in=comments, value__in=values)
    ratings_topics = Rating.objects.filter(topic__in=topics, value__in=values)
    ratings_map_topics = Rating.objects.filter(
        maptopic__in=map_topics, value__in=values
    )

    creator_objects = [
        comments,
        ratings_comments,
        ratings_ideas,
        ratings_map_ideas,
        ratings_topics,
        ratings_map_topics,
        ideas,
        map_ideas,
        votes,
        answers,
        proposals,
    ]

    rating_objects = [
        ratings_comments,
        ratings_map_ideas,
        ratings_topics,
        ratings_map_topics,
        ratings_ideas,
        likes,
    ]

    idea_objects = [ideas, map_ideas, proposals, topics, map_topics]

    insight, _ = ProjectInsight.objects.get_or_create(project=project)

    insight.comments = comments.count()
    insight.ratings = sum(x.count() for x in rating_objects)
    insight.written_ideas = sum(x.count() for x in idea_objects)
    insight.poll_answers = votes.count() + answers.count()
    insight.live_questions = live_questions.count()
    insight.save()

    insight.active_participants.clear()
    unregistered_participants = set()

    for obj in creator_objects:
        # ignore objects which don't have a creator, they are counted in the next step.
        ids = list(
            obj.filter(creator__isnull=False)
            .values_list("creator", flat=True)
            .distinct()
            .order_by()
        )
        insight.active_participants.add(*ids)
        # content from unregistered users doesn't have a creator but a content_id
        if model_field_exists(obj.model, "content_id"):
            content_ids = set(
                obj.filter(content_id__isnull=False)
                .values_list("content_id", flat=True)
                .distinct()
                .order_by()
            )
            unregistered_participants = unregistered_participants.union(content_ids)

    insight.unregistered_participants = len(unregistered_participants)
    return insight


def model_field_exists(cls, field):
    try:
        cls._meta.get_field(field)
        return True
    except FieldDoesNotExist:
        return False
