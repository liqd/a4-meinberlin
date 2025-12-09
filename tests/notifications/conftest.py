import pytest
from pytest_factoryboy import register

from meinberlin.test.factories import budgeting as budgeting_factories
from meinberlin.test.factories import ideas as ideas_factories
from meinberlin.test.factories import kiezradar
from meinberlin.test.factories import moderatorremarks as moderatorremarks_factories
from meinberlin.test.factories import newsletters

register(newsletters.FollowFactory)
register(budgeting_factories.ProposalFactory)
register(ideas_factories.IdeaFactory)
register(moderatorremarks_factories.ModeratorRemarkFactory)
register(kiezradar.SearchProfileFactory)
register(kiezradar.KiezradarQueryFactory)


@pytest.fixture
def search_factories(kiezradar_query_factory, search_profile_factory, user, user2):
    matching_profile = search_profile_factory(creator=user)
    non_matching_profile_same_user = search_profile_factory(creator=user)
    matching_profile_other_user = search_profile_factory(creator=user2)
    query1 = kiezradar_query_factory(text="Berlin")
    query2 = kiezradar_query_factory(text="Other")

    matching_profile.query = query1
    matching_profile.save()

    non_matching_profile_same_user.query = query2
    non_matching_profile_same_user.save()

    matching_profile_other_user.query = query1
    matching_profile_other_user.save()

    return matching_profile, non_matching_profile_same_user, matching_profile_other_user
