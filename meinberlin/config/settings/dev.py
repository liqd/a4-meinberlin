from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qid$h1o8&wh#p(j)lifis*5-rf@lbiy8%^3l4x%@b$z(tli@ab'

try:
    import debug_toolbar
except ImportError:
     pass
else:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INTERNAL_IPS = ('127.0.0.1', 'localhost')
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': '',
    }

try:
    from .local import *
except ImportError:
    pass

try:
    from .polygons import *
except ImportError:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
        'null': {
            'class': 'logging.NullHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'], 'level': 'INFO'
        },
        'raven': {
            'handlers': ['null'], 'level': 'ERROR'
        }
    }
}

try:
    INSTALLED_APPS += tuple(ADDITIONAL_APPS)
except NameError:
    pass

CSP_REPORT_ONLY = True
CSP_DEFAULT_SRC = ["'self'", "'unsafe-inline'", "'unsafe-eval'", 'data:', 'blob:', '*']
