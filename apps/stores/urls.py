# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from apps.stores.views import view_stores


urlpatterns = patterns('',

    (r'^stores/$',view_stores),

)
