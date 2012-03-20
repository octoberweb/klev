# -*- coding: utf-8 -*-
import os
import sys

activate_this = os.path.expanduser("/var/www/great/venv/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, os.path.expanduser("/var/www/"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'great.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


sys.path.append('/var/www/great/')
sys.path.append('/var/www/great/venv/lib/python2.6/site-packages/')

from django.core.handlers.wsgi import  WSGIHandler
application = WSGIHandler()
