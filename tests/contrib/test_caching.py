import pytest
from django.core.cache import cache
from django.http import HttpRequest
from django.urls import reverse

from adhocracy4.projects.enums import Access
from adhocracy4.test.factories import ProjectFactory
from meinberlin.apps.contrib import caching
from meinberlin.apps.projects.api import ProjectViewSet
from meinberlin.apps.projects.models import Project
from meinberlin.test.factories.extprojects import ExternalProjectFactory
from meinberlin.test.factories.plans import PlanFactory
from meinberlin.test.factories.projectcontainers import ProjectContainerFactory


@pytest.mark.skipif(not caching.REDIS_IS_ENABLED, reason="requires redis")
def test_delete_namespace():
    namespace = "test"
    value = "test_value"
    key = caching.get_key(namespace=namespace)
    cache.set(key=key, value=value, timeout=None)
    cache_value_before = cache.get(key)
    caching.delete(namespace=namespace)
    cache_value_after = cache.get(key)

    assert cache_value_before == value
    assert cache_value_after is None

    cache.clear()


@pytest.mark.skipif(not caching.REDIS_IS_ENABLED, reason="requires redis")
def test_delete_keys():
    keys = ["test1", "test2"]
    value = "test_value"

    for key in keys:
        cache.set(key=key, value=value, timeout=None)

    cache_value_before = cache.get(keys[0])
    deleted_keys = caching.delete(keys=keys)
    cache_value_after = cache.get(keys[0])

    assert cache_value_before == value
    assert cache_value_after is None
    assert deleted_keys == keys

    cache.clear()


@pytest.mark.django_db
@pytest.mark.skipif(not caching.REDIS_IS_ENABLED, reason="requires redis")
def test_add_or_query(project_factory):
    n_ideas = 3
    namespace = "test_projects"
    information = "test_information"
    filter_kwargs = {"information": information}
    project_factory.create_batch(size=n_ideas, information=information)
    cache_value_expected = Project.objects.filter(**filter_kwargs)
    key = caching.get_key(namespace=namespace)

    cache_value_before = cache.get(key=key)
    caching.add_or_query(
        namespace=namespace, query_set=Project.objects, filter_kwargs=filter_kwargs
    )
    cache_value_after = cache.get(key=key)

    assert cache_value_before is None
    assert list(cache_value_after) == list(cache_value_expected)

    cache.clear()


@pytest.mark.django_db
@pytest.mark.skipif(not caching.REDIS_IS_ENABLED, reason="requires redis")
def test_add_or_serialize():
    namespace = "test"
    key = caching.get_key(namespace=namespace)
    view_set = ProjectViewSet()
    view_set.request = HttpRequest()

    cache_value_before = cache.get(key=key)
    caching.add_or_serialize(namespace=namespace, view_set=view_set)
    cache_value_after = cache.get(key=key)

    assert cache_value_before is None
    assert cache_value_after == []

    cache.clear()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "namespace,url_name,factory,factory_kwargs",
    [
        ("projects", "projects-list", ProjectFactory, {}),
        ("plans", "plans-list", PlanFactory, {}),
        (
            "externalprojects",
            "extprojects-list",
            ExternalProjectFactory,
            {"access": Access.PUBLIC},
        ),
        ("projectcontainers", "containers-list", ProjectContainerFactory, {}),
    ],
)
@pytest.mark.skipif(not caching.REDIS_IS_ENABLED, reason="requires redis")
def test_calling_list_api_creates_cached_value(
    client, namespace, url_name, factory, factory_kwargs
):
    n_objects = 3
    url = reverse(url_name)
    cache_key = caching.get_key(namespace=namespace)
    cache_value_before = cache.get(cache_key)

    objects = factory.create_batch(size=n_objects, **factory_kwargs)
    response = client.get(url)
    cache_value_after = cache.get(cache_key)

    assert cache_value_before is None
    assert len(cache_value_after) == len(objects) == n_objects
    assert response.status_code == 200
    assert response.data == cache_value_after

    cache.clear()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "namespace,url_name,factory,factory_kwargs",
    [
        ("projects", "projects-list", ProjectFactory, {}),
        (
            "externalprojects",
            "extprojects-list",
            ExternalProjectFactory,
            {"access": Access.PUBLIC},
        ),
    ],
)
@pytest.mark.skipif(not caching.REDIS_IS_ENABLED, reason="requires redis")
def test_signal_triggers_cache_delete(
    client, namespace, url_name, factory, factory_kwargs
):
    n_objects = 3
    url = reverse(url_name)
    cache_key = caching.get_key(namespace=namespace)

    objects = factory.create_batch(size=n_objects, **factory_kwargs)
    response = client.get(url)
    cache_value_before = cache.get(cache_key)

    factory(**factory_kwargs)
    cache_value_after = cache.get(cache_key)

    assert response.status_code == 200
    assert len(cache_value_before) == len(objects) == n_objects
    assert cache_value_after is None

    cache.clear()
