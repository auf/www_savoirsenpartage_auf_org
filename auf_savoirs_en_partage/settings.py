# -*- encoding: utf-8 -*-

import os
from conf import *

ADMINS = (
    ('Équipe ARI-SI', 'developpeurs@ca.auf.org'),
    ('Éric Mc Sween', 'eric.mcsween@gmail.com')
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'fr-ca'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'pagination',
    'compressor',
    'django_roa',
    'savoirs',
    'chercheurs',
    'sitotheque',
    'djangosphinx',
    'datamaster_modeles'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default : http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#template-context-processors
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "context_processors.discipline_region",
    "djangoflash.context_processors.flash"
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

AUTHENTICATION_BACKENDS = ('authentification.AUFBackend', 'authentification.EmailBackend')
LOGIN_URL = '/chercheurs/connexion/'
LOGIN_REDIRECT_URL = '/chercheurs/perso/'

CACHE_BACKEND = 'memcached://localhost:11211'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

ROA_CUSTOM_ARGS = {'api-key': ROA_API_KEY}

ADMIN_TOOLS_INDEX_DASHBOARD = 'auf_savoirs_en_partage.dashboard.CustomIndexDashboard'

CONTACT_EMAIL = 'contact-savoirsenpartage@auf.org'

SPHINX_API_VERSION = 0x116
SPHINX_PORT = 9312

from auf_references_client.settings import *
