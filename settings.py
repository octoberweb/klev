# -*- coding: utf-8 -*-
try:
    from config.development import *
except ImportError:
    from config.production import *
    
    
INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    #'django.contrib.sitemaps',


    'django.contrib.admin',
    
    'apps.meta',
    #'apps.pages',
    'apps.products',
    'apps.stores',


    #'south',
    'pymorphy',
    'sorl.thumbnail',
)

    