from celery.schedules import crontab

from .base import *

DEBUG = False
DEFAULT_FROM_EMAIL = '"meinBerlin" <no-reply@mein.berlin.de>'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # defaut is 0 and is taken by celery for backend results
        "TIMEOUT": 86400,  # 24hrs
    }
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

try:
    from .local import *
except ImportError:
    pass

try:
    from .polygons import *
except ImportError:
    pass

try:
    INSTALLED_APPS += tuple(ADDITIONAL_APPS)
except NameError:
    pass

try:
    CKEDITOR_CONFIGS["collapsible-image-editor"]["embed_provider"] = CKEDITOR_URL
    CKEDITOR_CONFIGS["video-editor"]["embed_provider"] = CKEDITOR_URL
except NameError:
    pass

CELERY_BEAT_SCHEDULE = {
    "update-cache-for-projects-every-10-mim": {
        "task": "schedule_reset_cache_for_projects",
        "schedule": crontab(minute="*/10"),
    },
    "hourly-footer-update": {
        "task": "periodic_footer_update",
        "schedule": crontab(minute=0),
        "args": (),
    },
    "set-cache-for-projects-every-1-hr": {
        "task": "set_cache_for_projects",
        "schedule": crontab(minute=0, hour="*/1"),
        "args": (),
    },
    "periodic-notifications-cleanup-every-day-at-3am": {
        "task": "periodic_notifications_cleanup",
        "schedule": crontab(minute=0, hour="3"),
        "args": (),
    },
}
