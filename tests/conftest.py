import factory
import pytest
from django.urls import reverse
from pytest_factoryboy import register
from rest_framework.test import APIClient

from adhocracy4.test import factories as a4_factories
from adhocracy4.test import helpers
from adhocracy4.test.factories.maps import AreaSettingsFactory
from meinberlin.test import factories
from meinberlin.test.factories.activities import ActivityFactory
from meinberlin.test.factories.bplan import BplanFactory
from meinberlin.test.factories.extprojects import ExternalProjectFactory
from meinberlin.test.factories.likes import LikeFactory
from meinberlin.test.factories.organisations import OrganisationFactory
from meinberlin.test.factories.plans import PlanFactory
from meinberlin.test.factories.projectcontainers import ProjectContainerFactory


def pytest_configure(config):
    # Patch email background_task decorators for all tests
    helpers.patch_background_task_decorator('adhocracy4.emails.tasks')


register(factories.UserFactory)
register(factories.UserFactory, 'user2')
register(factories.AdminFactory, 'admin')
register(OrganisationFactory)
register(factories.CommentFactory)
register(factories.RatingFactory)
register(factories.ModeratorFeedbackFactory)
register(factories.CategoryFactory)
register(factories.AdministrativeDistrictFactory)
register(factories.LiveStreamFactory)
register(factories.LabelFactory)
register(ActivityFactory)
register(ProjectContainerFactory)
register(PlanFactory)
register(ExternalProjectFactory)
register(BplanFactory)
register(LikeFactory)

register(a4_factories.GroupFactory)
register(a4_factories.ProjectFactory)
register(a4_factories.PhaseFactory)
register(a4_factories.ModuleFactory)
register(AreaSettingsFactory)


@pytest.fixture
def apiclient():
    return APIClient()


@pytest.fixture
def smallImage():
    return factory.django.ImageField(width=200, height=200)


@pytest.fixture
def bigImage():
    return factory.django.ImageField(width=1400, height=1400)


@pytest.fixture
def ImageBMP():
    return factory.django.ImageField(width=1400, height=1400, format='BMP')


@pytest.fixture
def ImagePNG():
    return factory.django.ImageField(width=1400, height=1400, format='PNG')


@pytest.fixture
def image_factory():
    return factories.ImageFactory()


@pytest.fixture
def login_url():
    return reverse('account_login')


@pytest.fixture
def logout_url():
    return reverse('account_logout')


@pytest.fixture
def signup_url():
    return reverse('account_signup')
