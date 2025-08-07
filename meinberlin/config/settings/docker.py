from .dev import *
from .polygons import BERLIN_POLYGON

# Database settings
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "django",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": "5432",
    }
}

# Redis settings for Celery
REDIS_HOST = "redis"
REDIS_PORT = 6379

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# Debug settings
DEBUG = True
TEMPLATES[0]["OPTIONS"]["debug"] = True

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]
