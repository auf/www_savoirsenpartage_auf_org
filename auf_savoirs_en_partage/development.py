from auf_savoirs_en_partage.settings import *
DEBUG=True
TEMPLATE_DEBUG=DEBUG
INTERNAL_IPS = ('127.0.0.1',)
AUTH_PASSWORD_REQUIRED = False

# Activer la debug toolbar...

# MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# INSTALLED_APPS += ('debug_toolbar',)
# DEBUG_TOOLBAR_CONFIG = dict(INTERCEPT_REDIRECTS=False)
