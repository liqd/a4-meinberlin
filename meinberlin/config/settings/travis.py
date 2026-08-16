import os
import re

from .test import *


def _xdist_redis_location():
    """Separate Redis DB per pytest-xdist worker (cache.clear() flushes the whole DB)."""
    base = "redis://127.0.0.1:6379"
    worker = os.environ.get("PYTEST_XDIST_WORKER")
    if not worker:
        return f"{base}/1"
    match = re.fullmatch(r"gw(\d+)", worker)
    if match:
        return f"{base}/{int(match.group(1)) + 2}"
    return f"{base}/1"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": _xdist_redis_location(),
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "USER": "postgres",
        "NAME": "django",
        "TEST": {"NAME": "django_test"},
    }
}
