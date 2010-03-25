
import os
from conf import *

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
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

# Don't share this with anybody.
SECRET_KEY = 'k5m_cyht&ipi!nbxng9-5zc!4_q84opflhsn#d3%^3=9gm44tt'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'auf_savoirs_en_partage_django.urls'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django_roa',
    'auf_roa_authentification_backend',
    'savoirs',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

AUTHENTICATION_BACKENDS = (
    'auf_roa_authentification_backend.backends.CascadeBackend',
)
AUTH_PASSWORD_REQUIRED=True
ROA_MODELS = True   # set to False if you'd like to develop/test locally
ROA_FORMAT = 'django'
ROA_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
ROA_DJANGO_ERRORS = True # useful to ease debugging if you use test server

ROA_BASE_URL = 'https://authentification.auf.org/auth/'
ROA_CUSTOM_ARGS = {'api-key': ROA_API_KEY}

SERIALIZATION_MODULES = {
    'django' : 'auf_roa_authentification_backend.serializers',
}
