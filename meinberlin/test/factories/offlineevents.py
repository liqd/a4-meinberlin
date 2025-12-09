import factory
from dateutil.parser import parse

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.offlineevents import models


class OfflineEventItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OfflineEventItem

    name = factory.Faker("sentence", nb_words=3)
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory, blueprint_type="OE")
    event_type = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=200)
    event_date = parse("2013-01-02 00:00:00 UTC")
