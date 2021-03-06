# -*- encoding: utf-8 -*-

import os
from conf import *  # NOQA

PROJECT_HOME = os.path.dirname(__file__)
HOME = os.path.dirname(PROJECT_HOME)

DATE_FORMAT = "d b Y"

ADMINS = ()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

ADMINS_SEP = ('gilles.deggis@auf.org',)

MANAGERS = ADMINS

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr-ca'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_HOME, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
#    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auf.django.piwik.middleware.TrackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'chercheurs.middleware.ChercheurMiddleware',
    'djangoflash.middleware.FlashMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'auf_savoirs_en_partage.urls'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'pagination',
    'django_roa',
    'savoirs',
    'chercheurs',
    'sitotheque',
    'djangosphinx',
    'south',
    'raven.contrib.django',
    'auf.django.admingroup',
    'auf.django.references',
    'auf.django.pong',
    'alphafilter',
    'interfaces',
    'rappels',
    'pytz',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "context_processors.discipline_region",
    "djangoflash.context_processors.flash",
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_HOME, "templates"),
)

AUTHENTICATION_BACKENDS = (
    'auf.django.auth.backends.CascadeBackend',
    'authentification.PersonneBackend',
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_PROFILE_MODULE = 'savoirs.Profile'

LOGIN_URL = '/chercheurs/connexion/'
LOGIN_REDIRECT_URL = '/chercheurs/perso/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'localhost:11211'
    }
}

ADMIN_TOOLS_INDEX_DASHBOARD = \
        'auf_savoirs_en_partage.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_MENU = 'auf_savoirs_en_partage.menu.CustomMenu'

CONTACT_EMAIL = 'contact-savoirsenpartage@auf.org'

LOCALE_PATHS = (
    os.path.join(PROJECT_HOME, 'locale'),
)

SOUTH_TESTS_MIGRATE = False

# djangosphinx

SPHINX_API_VERSION = 0x116
SPHINX_PORT = 9312

# django.contrib.staticfiles

STATICFILES_DIRS = (
    os.path.join(PROJECT_HOME, 'static'),
)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(HOME, 'sitestatic')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_STORAGE = \
        'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
