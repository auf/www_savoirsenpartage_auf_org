from auf_savoirs_en_partage.settings import *
DEBUG=True
TEMPLATE_DEBUG=DEBUG
INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar',)
