import os
from .default import *


SECRET_KEY = os.getenv('SECRET_KEY', 'changeme')

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # tages
    'tages.authentication',
]
