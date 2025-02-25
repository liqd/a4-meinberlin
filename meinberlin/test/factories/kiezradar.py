import factory
from django.contrib.gis.geos import Point

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.kiezradar.models import KiezRadar
from meinberlin.apps.kiezradar.models import KiezradarQuery
from meinberlin.apps.kiezradar.models import ProjectStatus
from meinberlin.apps.kiezradar.models import ProjectType
from meinberlin.apps.kiezradar.models import SearchProfile


class SearchProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SearchProfile

    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    name = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("sentence", nb_words=16)

    @factory.post_generation
    def project_types(self, create, extracted, **kwargs):
        if extracted is not None:
            if isinstance(extracted, list):
                for project_type in extracted:
                    self.project_types.add(project_type)
            elif isinstance(extracted, int):
                self.project_types.add(ProjectType.objects.get(participation=extracted))
            else:
                self.project_types.add(extracted)

    @factory.post_generation
    def status(self, create, extracted, **kwargs):
        if extracted is not None:
            if isinstance(extracted, list):
                for project_status in extracted:
                    self.status.add(project_status)
            elif isinstance(extracted, int):
                self.status.add(ProjectStatus.objects.get(status=extracted))
            else:
                self.status.add(extracted)


class KiezRadarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KiezRadar

    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    name = factory.Faker("sentence", nb_words=4)
    point = Point(13.397788148643649, 52.52958586909979)
    radius = 500.0


class KiezradarQueryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KiezradarQuery

    text = factory.Faker("sentence", nb_words=8)


class ProjectTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectType

    participation = ProjectType.PARTICIPATION_CONSULTATION


class ProjectStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectStatus

    status = ProjectStatus.STATUS_ONGOING
