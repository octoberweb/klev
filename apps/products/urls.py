# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from apps.products.views import *


urlpatterns = patterns('',
    #(r'^$', countries_view),
    (r'^(?P<section_alias>[^/]+)/$',section_view),


)
