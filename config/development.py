# -*- coding: utf-8 -*-
import os
from config.base import *

# remove double slashes in url
#FORCE_SCRIPT_NAME = ""

DEBUG = True

#STATIC_ROOT = os.path.join(ROOT_PATH, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Asia/Yakutsk'
