# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

from apps.products.urls import urlpatterns as products_url
from apps.orders.urls import urlpatterns as orders_url
from apps.views import import_xml

urlpatterns = patterns('',

    url(r'^$', 'apps.views.index'),
    url(r'^import/', import_xml),
    url(r'^news/', include('apps.news.urls')),

)

urlpatterns += products_url + orders_url
#url(r'^services/', include('apps.services.urls')),

