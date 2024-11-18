from celery.schedules import crontab

from .base import *

DEBUG = False

# STORAGES = {
#    "default": {
#        "BACKEND": "django.core.files.storage.FileSystemStorage",
#    },
#    "staticfiles": {
#        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#    },
# }

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
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
SECRET_KEY = "asdasdasdoisadjsaoifjodsjgofdjgfdoig"
CSP_REPORT_ONLY = True
CSP_DEFAULT_SRC = ["'self'", "'unsafe-inline'", "'unsafe-eval'", "data:", "blob:", "*"]
