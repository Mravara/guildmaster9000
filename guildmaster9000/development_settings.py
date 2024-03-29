from .base_settings import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions'
]

MIDDLEWARE += [
    # django toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }