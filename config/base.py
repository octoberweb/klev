# -*- coding: utf-8 -*-
import os

PROJECT_NAME = 'klev'

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ROOT_PATH + '/static/'
STATIC_DOC_ROOT = ROOT_PATH + '/static/'
MEDIA_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_ROOT = ROOT_PATH + '/media/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n56Uidrtu}ig%#hgjh$pbdvwlju7b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'apps.pages.middleware.PageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    #'django.core.context_processors.i18n',
    #'django.core.context_processors.media',
    #'django.core.context_processors.static',
    #'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    #'apps.utils.context_processors.custom_proc',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    #os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
    os.path.join(ROOT_PATH, 'templates')
)

ADMIN_TOOLS_MENU = 'menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'dashboard.CustomAppIndexDashboard'




ACCOUNT_ACTIVATION_DAYS = 7 # кол-во дней для хранения кода активации
AUTH_USER_EMAIL_UNIQUE = False
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = u'support@%s.ru' % PROJECT_NAME
LOGIN_REDIRECT_URL = '/'



PYMORPHY_DICTS = {
    'ru': {
        'dir': os.path.join(ROOT_PATH, 'files', 'dicts')
    },
    }

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.


FIRST_DAY_OF_WEEK = 1