from io import BytesIO

import factory
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.files import base
from django.core.files import images
from PIL import Image

from adhocracy4 import phases
from adhocracy4.test import factories


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('name')
    password = make_password('password')
    email = factory.Faker('email')


class AdminFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('name')
    password = make_password('password')
    is_superuser = True


# FIXME: move to core
class PhaseContentFactory(factory.Factory):
    class Meta:
        model = phases.PhaseContent

    app = 'phase_content_factory'
    phase = 'factory_phase'
    weight = 10
    view = None

    name = 'Factory Phase'
    description = 'Factory Phase Description'
    module_name = 'factory phase module'

    features = {}

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        phase_content = model_class()
        for key, value in kwargs.items():
            setattr(phase_content, key, value)

        phases.content.register(phase_content)
        return phase_content


# FIXME: move to core
class PhaseFactory(factories.PhaseFactory):

    class Params:
        phase_content = PhaseContentFactory()

    type = factory.LazyAttribute(lambda f: f.phase_content.identifier)


class OrganisationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'meinberlin_organisations.Organisation'
        django_get_or_create = ('name',)

    name = factory.Faker('company')

    @factory.post_generation
    def initiators(self, create, extracted, **kwargs):
        if not extracted:
            user = UserFactory()
            self.initiators.add(user)
            return

        if extracted:
            for user in extracted:
                self.initiators.add(user)


class ImageFactory():
    """Create a django file object containg an image."""

    def __call__(self, resolution, image_format='JPEG', name=None):

        filename = name or 'default.{}'.format(image_format.lower())
        color = 'blue'
        image = Image.new('RGB', resolution, color)
        image_data = BytesIO()
        image.save(image_data, image_format)
        image_content = base.ContentFile(image_data.getvalue())
        return images.ImageFile(image_content.file, filename)


class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'a4comments.Comment'

    comment = factory.Faker('text')
    creator = factory.SubFactory(UserFactory)


class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'a4ratings.Rating'

    value = 1
    creator = factory.SubFactory(UserFactory)


class ModeratorStatementFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'meinberlin_moderatorfeedback.ModeratorStatement'

    statement = factory.Faker('text')
    creator = factory.SubFactory(UserFactory)


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'a4categories.Category'

    name = factory.Faker('job')
    module = factory.SubFactory(factories.ModuleFactory)
