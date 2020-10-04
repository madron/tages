from .common import *


# Debug Toolbar
INSTALLED_APPS += [
    'debug_toolbar',
    'graphiql_debug_toolbar',
]
MIDDLEWARE.insert(1, 'graphiql_debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']
