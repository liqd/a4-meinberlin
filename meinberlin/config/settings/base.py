"""
Django settings for meinberlin project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.utils.translation import gettext_lazy as _

CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(CONFIG_DIR)
BASE_DIR = os.path.dirname(PROJECT_DIR)

# General settings

CONTACT_EMAIL = "support-berlin@liqd.net"
SUPERVISOR_EMAIL = "berlin-supervisor@liqd.net"
TRACKING_ENABLED = False

# Application definition

INSTALLED_APPS = (
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtail.contrib.styleguide",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "background_task",
    "ckeditor",
    "ckeditor_uploader",
    "django_filters",
    "easy_thumbnails",
    "rest_framework",
    "rules.apps.AutodiscoverRulesConfig",
    "taggit",  # wagtail dependency
    "widget_tweaks",
    "adhocracy4.actions",
    "adhocracy4.administrative_districts",
    "adhocracy4.categories",
    "adhocracy4.ckeditor",
    "adhocracy4.comments",  # needed for comment model
    "adhocracy4.comments_async",
    "adhocracy4.dashboard",
    "adhocracy4.exports",
    "adhocracy4.filters",
    "adhocracy4.follows",
    "adhocracy4.forms",
    "adhocracy4.images",
    "adhocracy4.labels",
    "adhocracy4.maps",
    "adhocracy4.modules",
    "adhocracy4.organisations",
    "adhocracy4.phases",
    "adhocracy4.polls",
    "adhocracy4.projects",
    "adhocracy4.ratings",
    "adhocracy4.reports",
    "adhocracy4.rules",
    # General components that define models or helpers
    "meinberlin.apps.actions",
    "meinberlin.apps.captcha",
    "meinberlin.apps.cms",
    "meinberlin.apps.contrib",
    "meinberlin.apps.likes",
    "meinberlin.apps.livequestions",
    "meinberlin.apps.maps",
    "meinberlin.apps.moderationtasks",
    "meinberlin.apps.moderatorfeedback",
    "meinberlin.apps.moderatorremark",
    "meinberlin.apps.notifications",
    "meinberlin.apps.organisations",
    "meinberlin.apps.users",
    "meinberlin.apps.votes",
    # General apps containing views
    "meinberlin.apps.account",
    "meinberlin.apps.adminlog",
    "meinberlin.apps.dashboard",
    "meinberlin.apps.embed",
    "meinberlin.apps.initiators",
    "meinberlin.apps.newsletters",
    "meinberlin.apps.offlineevents",
    "meinberlin.apps.plans",
    "meinberlin.apps.platformemails",
    # Apps defining phases
    "meinberlin.apps.activities",
    "meinberlin.apps.bplan",
    "meinberlin.apps.budgeting",
    "meinberlin.apps.documents",
    "meinberlin.apps.extprojects",
    "meinberlin.apps.ideas",
    "meinberlin.apps.kiezkasse",
    "meinberlin.apps.mapideas",
    "meinberlin.apps.maptopicprio",
    "meinberlin.apps.projectcontainers",
    "meinberlin.apps.topicprio",
    # Apps overwriting and adding to a4
    "meinberlin.apps.polls",
    "meinberlin.apps.projects",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_cloudflare_push.middleware.push_middleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "meinberlin.apps.embed.middleware.AjaxPathMiddleware",
    "meinberlin.apps.votes.middleware.VotingTokenSessionMiddleware",
)

SITE_ID = 1

ROOT_URLCONF = "meinberlin.config.urls"

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "meinberlin.config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# FIXME: use custom engine to work around a bug on m1 macbooks
# can be set back to djangos sqlite3 backend once upgrade to >=4.1 is done
DATABASES = {
    "default": {
        "ENGINE": "sqlite_m1",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "TEST": {
            "NAME": os.path.join(BASE_DIR, "test_db.sqlite3"),
        },
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "de-DE"

# The default language is used for emails and strings
# that are stored translated to the database.
DEFAULT_LANGUAGE = "de"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

IMAGE_ALIASES = {
    "*": {
        "max_size": 5 * 10**6,
        "fileformats": ("image/png", "image/jpeg", "image/gif"),
    },
    "heroimage": {"min_resolution": (1500, 500)},
    "tileimage": {"min_resolution": (500, 300)},
    "logo": {"min_resolution": (200, 50)},
    "avatar": {"min_resolution": (200, 200)},
    "idea_image": {"min_resolution": (600, 400)},
    "plan_image": {"min_resolution": (600, 400)},
}

THUMBNAIL_ALIASES = {
    "": {
        "heroimage": {"size": (1500, 500)},
        "project_thumbnail": {"size": (520, 330)},
        "logo": {"size": (160, 160), "background": "white"},
        "item_image": {"size": (330, 0), "crop": "scale"},
        "map_thumbnail": {"size": (200, 200), "crop": "smart"},
        "plan_image": {"size": (600, 400)},
        "project_tile": {"size": (500, 500)},
    }
}

ALLOWED_UPLOAD_IMAGES = ("png", "jpeg", "gif")

# default primary field for models without that field set

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Wagtail settings

WAGTAIL_SITE_NAME = "meinBerlin"
WAGTAILIMAGES_IMAGE_MODEL = "meinberlin_cms.CustomImage"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

# Authentication

AUTH_USER_MODEL = "meinberlin_users.User"

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_ADAPTER = "meinberlin.apps.users.adapters.AccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_FORMS = {"signup": "meinberlin.apps.users.forms.TermsSignupForm"}
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # seconds
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_PREVENT_ENUMERATION = True
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_FORMS = {"signup": "meinberlin.apps.users.forms.SocialTermsSignupForm"}
SOCIALACCOUNT_QUERY_EMAIL = True
# This is currently needed for servicekonto account connection
SESSION_COOKIE_SAMESITE = None

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "/"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_RESTRICT_BY_USER = "username"
CKEDITOR_ALLOW_NONIMAGE_FILES = True
CKEDITOR_EMBED_PROVIDER = ""

CKEDITOR_CONFIGS = {
    "default": {
        "width": "100%",
        "title": _("Rich text editor"),
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            ["NumberedList", "BulletedList"],
            ["Link", "Unlink"],
        ],
        "removePlugins": "stylesheetparser",
        "extraAllowedContent": "iframe[*]",
        "extraPlugins": ",".join(["embed", "embedbase"]),
    },
    "image-editor": {
        "width": "100%",
        "title": _("Rich text editor"),
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            ["Image"],
            ["NumberedList", "BulletedList"],
            ["Link", "Unlink"],
        ],
    },
    "collapsible-image-editor": {
        "width": "100%",
        "title": _("Rich text editor"),
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            ["Image"],
            ["NumberedList", "BulletedList"],
            ["Link", "Unlink"],
            ["CollapsibleItem"],
            ["Embed", "EmbedBase"],
        ],
        "removePlugins": "stylesheetparser",
        "extraAllowedContent": "iframe[*]; div[*]",
        "embed_provider": CKEDITOR_EMBED_PROVIDER,
    },
    "video-editor": {
        "width": "100%",
        "title": _("Rich text editor"),
        "toolbar": "Custom",
        "toolbar_Custom": [["Embed", "EmbedBase"]],
        "removePlugins": "stylesheetparser",
        "extraAllowedContent": "iframe[*]; div[*]",
        "embed_provider": CKEDITOR_EMBED_PROVIDER,
    },
}

BLEACH_LIST = {
    "default": {
        "tags": [
            "p",
            "strong",
            "em",
            "u",
            "ol",
            "li",
            "ul",
            "a",
            "img",
            "iframe",
            "div",
        ],
        "attributes": {
            "a": ["href", "rel", "target"],
            "img": ["src", "alt", "style"],
            "div": ["class"],
            "iframe": ["src", "alt", "style"],
        },
    },
    "image-editor": {
        "tags": ["p", "strong", "em", "u", "ol", "li", "ul", "a", "img"],
        "attributes": {"a": ["href", "rel", "target"], "img": ["src", "alt", "style"]},
        "styles": [
            "float",
            "margin",
            "padding",
            "width",
            "height",
            "margin-bottom",
            "margin-top",
            "margin-left",
            "margin-right",
        ],
    },
    "collapsible-image-editor": {
        "tags": [
            "p",
            "strong",
            "em",
            "u",
            "ol",
            "li",
            "ul",
            "a",
            "img",
            "div",
            "iframe",
        ],
        "attributes": {
            "a": ["href", "rel", "target"],
            "img": ["src", "alt", "style"],
            "div": ["class"],
            "iframe": ["src", "alt", "style"],
        },
        "styles": [
            "float",
            "margin",
            "padding",
            "width",
            "height",
            "margin-bottom",
            "margin-top",
            "margin-left",
            "margin-right",
        ],
    },
    "video-editor": {
        "tags": ["a", "img", "div", "iframe"],
        "attributes": {
            "a": ["href", "rel", "target"],
            "img": ["src", "alt", "style"],
            "div": ["class"],
            "iframe": ["src", "alt", "style"],
        },
    },
}


# adhocracy4

A4_ORGANISATIONS_MODEL = "meinberlin_organisations.Organisation"

A4_RATEABLES = (
    ("a4comments", "comment"),
    ("meinberlin_ideas", "idea"),
    ("meinberlin_mapideas", "mapidea"),
    ("meinberlin_budgeting", "proposal"),
    ("meinberlin_kiezkasse", "proposal"),
    ("meinberlin_topicprio", "topic"),
    ("meinberlin_maptopicprio", "maptopic"),
)

A4_COMMENTABLES = (
    ("a4comments", "comment"),
    ("a4polls", "poll"),
    ("meinberlin_ideas", "idea"),
    ("meinberlin_mapideas", "mapidea"),
    ("meinberlin_budgeting", "proposal"),
    ("meinberlin_kiezkasse", "proposal"),
    ("meinberlin_topicprio", "topic"),
    ("meinberlin_maptopicprio", "maptopic"),
    ("meinberlin_documents", "chapter"),
    ("meinberlin_documents", "paragraph"),
)

A4_REPORTABLES = (
    ("a4comments", "comment"),
    ("meinberlin_ideas", "idea"),
    ("meinberlin_mapideas", "mapidea"),
    ("meinberlin_budgeting", "proposal"),
    ("meinberlin_kiezkasse", "proposal"),
)

A4_ACTIONABLES = (
    ("a4comments", "comment"),
    ("meinberlin_ideas", "idea"),
    ("meinberlin_mapideas", "mapidea"),
    ("meinberlin_budgeting", "proposal"),
    ("meinberlin_kiezkasse", "proposal"),
)

A4_AUTO_FOLLOWABLES = (
    # Disabled to keep current behaviour: the auto follow functionality did
    # not work until 2018/03/21 due to a adhocracy4 bug
    # ('a4comments', 'comment'),
    # ('meinberlin_ideas', 'idea'),
    # ('meinberlin_mapideas', 'mapidea'),
    # ('meinberlin_budgeting', 'proposal'),
    # ('meinberlin_kiezkasse', 'proposal'),
)

A4_CATEGORIZABLE = (
    ("meinberlin_ideas", "idea"),
    ("meinberlin_mapideas", "mapidea"),
    ("meinberlin_budgeting", "proposal"),
    ("meinberlin_kiezkasse", "proposal"),
    ("meinberlin_topicprio", "topic"),
    ("meinberlin_maptopicprio", "maptopic"),
)

A4_LABELS_ADDABLE = (
    ("meinberlin_ideas", "idea"),
    ("meinberlin_mapideas", "mapidea"),
    ("meinberlin_budgeting", "proposal"),
    ("meinberlin_kiezkasse", "proposal"),
    ("meinberlin_topicprio", "topic"),
    ("meinberlin_maptopicprio", "maptopic"),
)

A4_CATEGORY_ICONS = (
    ("", _("Pin without icon")),
    ("diamant", _("Diamond")),
    ("dreieck_oben", _("Triangle up")),
    ("dreieck_unten", _("Triangle down")),
    ("ellipse", _("Ellipse")),
    ("halbkreis", _("Semi circle")),
    ("hexagon", _("Hexagon")),
    ("parallelogramm", _("Rhomboid")),
    ("pentagramm", _("Star")),
    ("quadrat", _("Square")),
    ("raute", _("Octothorpe")),
    ("rechtecke", _("Rectangle")),
    ("ring", _("Circle")),
    ("rw_dreieck", _("Right triangle")),
    ("zickzack", _("Zigzag")),
)

A4_USE_VECTORMAP = True
A4_MAP_BASEURL = "https://basemap.berlin.de/gdz_basemapde_vektor/styles/bm_web_col.json"
A4_OPENMAPTILES_TOKEN = "9aVUrssbx7PKNUKo3WtXY6MqETI6Q336u5D142QS"
A4_MAPBOX_TOKEN = ""

A4_PROJECT_TOPICS = (
    ("ANT", _("Anti-discrimination")),
    ("WOR", _("Work & economy")),
    ("BUI", _("Building & living")),
    ("EDU", _("Education & research")),
    ("CHI", _("Children, youth & family")),
    ("FIN", _("Finances")),
    ("HEA", _("Health & sports")),
    ("INT", _("Integration")),
    ("CUL", _("Culture & leisure")),
    ("NEI", _("Neighborhood & participation")),
    ("URB", _("Urban development")),
    ("ENV", _("Environment & public green space")),
    ("TRA", _("Traffic")),
)

A4_BLUEPRINT_TYPES = [
    ("BS", "brainstorming"),
    ("MBS", "map brainstorming"),
    ("IC", "idea collection"),
    ("MIC", "map idea collection"),
    ("PB", "participatory budgeting (1 phase)"),
    ("PB2", "participatory budgeting (2 phase)"),
    ("PB3", "participatory budgeting (3 phase)"),
    ("KK", "kiezkasse"),
    ("TP", "topic prioritization"),
    ("MTP", "map topic prioritization"),
    ("TR", "text review"),
    ("PO", "poll"),
    ("IE", "interactive event"),
    ("EP", "external project"),
    ("BP", "bebauungsplan"),
    ("PC", "project container"),
]

A4_MAP_BOUNDING_BOX = [[52.3517, 13.8229], [52.6839, 12.9543]]

A4_DASHBOARD = {
    "PROJECT_DASHBOARD_CLASS": "meinberlin.apps.dashboard.TypedProjectDashboard",
    "BLUEPRINTS": "meinberlin.apps.dashboard.blueprints.blueprints",
}

A4_ACTIONS_PHASE_ENDS_HOURS = 48

# Add a Captcheck captcha URL in the production server's local.py to use it
# Captcha software we use: https://source.netsyms.com/Netsyms/Captcheck
CAPTCHA_URL = ""

# Celery configuration
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_EXTENDED = True

# BO external footer
BERLIN_FOOTER_FILENAME = "landesfooter.inc"
BERLIN_FOOTER_URL = (
    "https://www.berlin.de/rbmskzl/aktuelles/__i9/std/landesfooter.inc?js=0?css=0"
)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
