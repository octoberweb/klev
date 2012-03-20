# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from apps.news.views import *


urlpatterns = patterns('',
    (r'^$',news_list),
    (r'(?P<news_id>\d+)/$',news_detail),

)