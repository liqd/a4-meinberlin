from pytest_factoryboy import register

from meinberlin.test.factories import budgeting
from meinberlin.test.factories import ideas

register(ideas.IdeaFactory)
register(budgeting.ProposalFactory)
