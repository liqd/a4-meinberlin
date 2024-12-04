import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.kiezradar.models import KiezradarQuery
from meinberlin.apps.kiezradar.models import ProjectType
from meinberlin.apps.kiezradar.models import SearchProfile


class SearchProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SearchProfile

    user = factory.SubFactory(a4_factories.USER_FACTORY)
    name = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("sentence", nb_words=16)
    status = SearchProfile.STATUS_ONGOING


class KiezradarQueryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KiezradarQuery

    text = factory.Faker("sentence", nb_words=8)


class ProjectTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectType

    participation = ProjectType.PARTICIPATION_INFORMATION
