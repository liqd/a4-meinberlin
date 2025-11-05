from pytest_factoryboy import register

from adhocracy4.test.factories import polls as polls_factory
from meinberlin.test.factories import budgeting
from meinberlin.test.factories import ideas
from meinberlin.test.factories.documents import ChapterFactory
from meinberlin.test.factories.likes import LikeFactory
from meinberlin.test.factories.livequestions import LiveQuestionFactory
from meinberlin.test.factories.mapideas import MapIdeaFactory
from meinberlin.test.factories.maptopicprio import MaptopicFactory
from meinberlin.test.factories.topicprio import TopicFactory

from . import factories as invites

register(invites.ModeratorInviteFactory)
register(invites.ParticipantInviteFactory)
register(invites.ProjectInsightFactory)
register(ideas.IdeaFactory)
register(budgeting.ProposalFactory)
register(polls_factory.PollFactory)
register(polls_factory.QuestionFactory)
register(polls_factory.AnswerFactory)
register(polls_factory.ChoiceFactory)
register(polls_factory.VoteFactory)
register(TopicFactory)
register(LiveQuestionFactory)
register(LikeFactory)
register(ChapterFactory)
register(MapIdeaFactory)
register(MaptopicFactory)
