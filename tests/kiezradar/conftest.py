from pytest_factoryboy import register

from meinberlin.test.factories.kiezradar import KiezradarQueryFactory
from meinberlin.test.factories.kiezradar import ProjectStatusFactory
from meinberlin.test.factories.kiezradar import ProjectTypeFactory
from meinberlin.test.factories.kiezradar import SearchProfileFactory
from meinberlin.test.factories.organisations import OrganisationFactory

register(SearchProfileFactory)
register(KiezradarQueryFactory)
register(ProjectTypeFactory)
register(ProjectStatusFactory)
register(OrganisationFactory)
