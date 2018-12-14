import factory

from adhocracy4.test import factories as a4_factories
from adhocracy4.test.factories import AdministrativeDistrictFactory
from meinberlin.apps.plans.models import Plan


class PlanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Plan

    title = factory.Faker('sentence')
    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    organisation = factory.SubFactory(a4_factories.ORGANISATION_FACTORY)
    district = factory.SubFactory(AdministrativeDistrictFactory)
    point = {
        'type': 'Feature',
        'properties': {},
        'geometry': {'type': 'Point',
                     'coordinates': [13.447437286376953, 52.51518602243137]}
    }
    contact = ''
    theme = ''
    status = Plan.STATUS_TODO
    participation = Plan.PARTICIPATION_UNDECIDED

    @factory.post_generation
    def projects(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for project in extracted:
                self.projects.add(project)
