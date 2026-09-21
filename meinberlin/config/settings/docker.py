import os

from .dev import *

DEBUG = False

for template_engine in TEMPLATES:
    template_engine["OPTIONS"]["debug"] = False

INSTALLED_APPS = tuple(app for app in INSTALLED_APPS if app != "debug_toolbar")
MIDDLEWARE = tuple(
    middleware
    for middleware in MIDDLEWARE
    if middleware != "debug_toolbar.middleware.DebugToolbarMiddleware"
)

# PostgreSQL with PostGIS (service name "db" in docker-compose)
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("POSTGRES_DB", "django"),
        "USER": os.environ.get("POSTGRES_USER", "django"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "django"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("CACHE_URL", "redis://redis:6379/1"),
        "TIMEOUT": 86400,  # 24hrs
    }
}

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
CELERY_TASK_ALWAYS_EAGER = False

# Celery default concurrency is the number of CPU cores, which lets a single
# container balloon to several GiB on large hosts. Bound it (each prefork child
# loads a full Django instance) and recycle children so long-running workers do
# not accumulate memory. All values are overridable per environment via env
# vars (e.g. in Coolify).
CELERY_WORKER_CONCURRENCY = int(os.environ.get("CELERY_WORKER_CONCURRENCY", "1"))
CELERY_WORKER_MAX_TASKS_PER_CHILD = int(
    os.environ.get("CELERY_WORKER_MAX_TASKS_PER_CHILD", "100")
)
CELERY_WORKER_MAX_MEMORY_PER_CHILD = int(
    os.environ.get("CELERY_WORKER_MAX_MEMORY_PER_CHILD", "400")
)
CELERY_WORKER_PREFETCH_MULTIPLIER = int(
    os.environ.get("CELERY_WORKER_PREFETCH_MULTIPLIER", "1")
)
CELERY_WORKER_POOL = os.environ.get("CELERY_WORKER_POOL", "prefork")

# Periodic tasks are defined in production.py; reuse them for the container.
from .production import CELERY_BEAT_SCHEDULE  # noqa: E402,F401

ALLOWED_HOSTS = ["*"]

WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "http://localhost:8003")

# TLS terminates at the reverse proxy (Traefik/Nginx); trust its
# X-Forwarded-Proto so Django sees the original scheme. Required for the CSRF
# origin check when logging in over HTTPS.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Instance-specific settings, rendered by Salt into a .env file inside the
# named volume mounted at /data (docker-compose.yml). Coolify overrides
# container env vars, so the file is read directly instead of via os.environ.
import json  # noqa: E402

from dotenv import dotenv_values  # noqa: E402

_MEINBERLIN_INSTANCE_ENV = dotenv_values("/data/.env") or {}


def _load_json_value(name, default="{}"):
    raw = _MEINBERLIN_INSTANCE_ENV.get(name)
    if not raw:
        return json.loads(default)
    return json.loads(raw)


globals().update(_load_json_value("MEINBERLIN_CONFIG"))
