# -*- coding: utf-8 -*-

# import django
import os

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-treenode'

ALLOWED_HOSTS = ['*']

database_engine = os.environ.get('DATABASE_ENGINE', 'sqlite')
database_config = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    # 'mysql': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'treenode',
    #     'USER': 'mysql',
    #     'PASSWORD': 'mysql',
    #     'HOST': '',
    #     'PORT': '',
    # },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'treenode',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '',
    }
}

DATABASES = {
    'default': database_config.get(database_engine),
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'tests',
    'treenode',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'treenode/public/media/')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'treenode/public/static/')
STATIC_URL = '/static/'
