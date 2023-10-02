from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import redis
from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from meinberlin.apps import logger

ONE_HOUR = 3600
CACHE_SETTINGS = settings.CACHES.get("default", {})
DEFAULT_TIMEOUT = CACHE_SETTINGS.get("DEFAULT_TIMEOUT", ONE_HOUR)
CACHE_KEY_PREFIX = CACHE_SETTINGS.get("CACHE_KEY_PREFIX", "api_cache")
CACHE_LOCATION = CACHE_SETTINGS.get("LOCATION", "")
REDIS_IS_ENABLED = "redis" in CACHE_LOCATION
REDIS_CLIENT = redis.from_url(url=CACHE_LOCATION) if REDIS_IS_ENABLED else None

logger.info(
    f"cache startup: {REDIS_IS_ENABLED=}, {CACHE_LOCATION=}, {CACHE_KEY_PREFIX=}, {DEFAULT_TIMEOUT=}"
)


def create_key(namespace: str, suffix: str = "") -> str:
    terms = [x for x in [CACHE_KEY_PREFIX, namespace, suffix] if x]
    return "_".join(terms)


def delete(
    namespace: str = "",
    context: Optional[dict] = None,
    keys: Optional[List[str]] = None,
) -> List[str]:
    keys = keys or []

    if REDIS_IS_ENABLED and namespace:
        pattern = f"*{create_key(namespace=namespace)}*"
        keys = REDIS_CLIENT.keys(pattern=pattern)
        if keys:
            REDIS_CLIENT.delete(*keys)

        logger.info(f"cache delete: {namespace=}, {pattern=}, {len(keys)=}, {context=}")

    elif keys:
        for key in keys:
            cache.delete(key)

        logger.info(f"cache delete: {len(keys)=}, {context=}")

    else:
        logger.warning(f"cache delete failed: {namespace=}, {keys=}, {context=}")

    return keys


def add_or_query(
    namespace: str,
    query_set: QuerySet,
    filter_kwargs: Optional[Dict[str, Any]] = None,
    suffix: str = "",
    timeout: int = DEFAULT_TIMEOUT,
) -> QuerySet:
    filter_kwargs = filter_kwargs or {}
    key = create_key(namespace=namespace, suffix=suffix)
    filtered_query = cache.get(key)

    if filtered_query is None:
        logger.info(f"cache missed: {key=}")
        filtered_query = query_set.filter(**filter_kwargs)
        cache.set(key=key, value=filtered_query, timeout=timeout)

    return filtered_query


def add_or_serialize(
    namespace: str,
    view_set: GenericViewSet,
    context: Optional[dict] = None,
    suffix: str = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Response:
    key = create_key(namespace=namespace, suffix=suffix)
    data = cache.get(key)

    if not data:
        logger.info(f"cache missed: {key=}, {context=}")
        queryset = view_set.filter_queryset(queryset=view_set.get_queryset())
        serializer = view_set.get_serializer(queryset, many=True)
        data = serializer.data
        cache.set(key=key, value=data, timeout=timeout)

    return Response(data)
