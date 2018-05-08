# -*- coding: utf-8 -*-

import django
import os

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-treenode'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'tests',
    'treenode',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'treenode/public/media/')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'treenode/public/static/')
STATIC_URL = '/static/'
