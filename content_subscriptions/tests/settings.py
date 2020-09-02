"""
Based off of https://github.com/Fantomas42/django-tagging/blob/develop/tagging/tests/settings.py
"""

import os

SECRET_KEY = 'my-super-secret-key'

DATABASES = {
    'default': {
        'NAME': 'subscriptions.db',
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE')
if DATABASE_ENGINE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'subscriptions',
            'USER': 'postgres',
            'HOST': 'localhost'
        }
    }
elif DATABASE_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'subscriptions',
            'USER': 'root',
            'HOST': 'localhost',
            'TEST': {
                'COLLATION': 'utf8_general_ci'
            }
        }
    }

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'content_subscriptions',
    'content_subscriptions.tests',
]

AUTH_USER_MODEL = 'tests.ExtendedUser'
SUBSCRIPTION_HOLDER_MODEL = 'tests.ExtendedUser'
