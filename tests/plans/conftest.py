from pytest_factoryboy import register

from adhocracy4.test.factories import ProjectFactory
from meinberlin.test.factories import maps as map_factories
from meinberlin.test.factories import plans as plan_factories

register(ProjectFactory)
register(map_factories.MapPresetCategoryFactory)
register(map_factories.MapPresetFactory)
register(plan_factories.PlanFactory)
