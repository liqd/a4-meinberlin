import factory

from adhocracy4.test import factories as a4_factories
from meinberlin.apps.bplan import models as bplan_models


class BplanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = bplan_models.Bplan

    name = factory.Faker("sentence", nb_words=4)
    office_worker_email = factory.Faker("email")
    organisation = factory.SubFactory(a4_factories.ORGANISATION_FACTORY)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Ensure there's always an administrative_district
        if "administrative_district" not in kwargs:
            from adhocracy4.administrative_districts.models import (
                AdministrativeDistrict,
            )

            district, _ = AdministrativeDistrict.objects.get_or_create(
                name="Mitte", short_code="mi"
            )
            kwargs["administrative_district"] = district
        return super()._create(model_class, *args, **kwargs)
