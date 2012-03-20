# -*- coding: utf-8 -*-

import os

from config.base import *

# remove double slashes in url
FORCE_SCRIPT_NAME = ""

DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATIC_ROOT = os.path.join(ROOT_PATH, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'great',
        'USER': 'great',
        'PASSWORD': 'youpass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

DATABASE_ENGINE = 'postgresql_psycopg2'
