from pytest_factoryboy import register

from meinberlin.test.factories import budgeting as budgeting_factories
from meinberlin.test.factories import ideas as ideas_factories
from meinberlin.test.factories import moderatorremarks as moderatorremarks_factories
from meinberlin.test.factories import newsletters
from meinberlin.test.factories import offlineevents

register(newsletters.FollowFactory)
register(budgeting_factories.ProposalFactory)
register(ideas_factories.IdeaFactory)
register(offlineevents.OfflineEventFactory)
register(moderatorremarks_factories.ModeratorRemarkFactory)
