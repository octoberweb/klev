# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from apps.views import import_xml

urlpatterns = patterns('',

    url(r'^$', 'apps.views.index'),
    url(r'^section/', include('apps.products.urls')),
    url(r'^import/', import_xml),

)


#url(r'^services/', include('apps.services.urls')),

