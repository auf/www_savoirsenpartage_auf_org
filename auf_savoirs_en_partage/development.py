from auf_savoirs_en_partage.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

# Debug toolbar

# MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# INSTALLED_APPS += ('debug_toolbar',)
# DEBUG_TOOLBAR_CONFIG = dict(INTERCEPT_REDIRECTS=True)

# Profiling

MIDDLEWARE_CLASSES = ('savoirs.middleware.ProfileMiddleware',) + MIDDLEWARE_CLASSES

# css/js compression

# COMPRESS = True
