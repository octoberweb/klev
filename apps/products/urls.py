# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from apps.countries.views import *


urlpatterns = patterns('',
    (r'^$', countries_view),
    (r'^(?P<country_alias>[^/]+)/$',country_view),


)
