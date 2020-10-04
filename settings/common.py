import os
from .default import *


SECRET_KEY = os.getenv('SECRET_KEY', 'changeme')
VERSION = os.getenv('VERSION', 'dev')

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'reversion',
    'import_export',
    'graphene_django',
    'django_filters',
    # tages
    'tages.authentication',
    'tages.countries',
    'tages.registries',
    'tages.utils',
    'tages.graphql',
]

GRAPHENE = {
    'SCHEMA': 'tages.graphql.schema.schema',
}
