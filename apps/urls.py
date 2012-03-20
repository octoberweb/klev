# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'apps.views.index'),

)


#url(r'^services/', include('apps.services.urls')),

