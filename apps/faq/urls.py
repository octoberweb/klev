# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from faq.views import *


urlpatterns = patterns('',


    ('^faq/page/(?P<page>\d+)/$',questions_list),
    ('^faq/page/$',questions_list),

    ('^faq/(?P<category_alias>[A-Za-z0-9-]+)/page/(?P<page>\d+)/$',questions_list),
    ('^faq/(?P<category_alias>[A-Za-z0-9-]+)/$',questions_list),

    ('^faq/$',questions_list),

    ('^feedback/page/(?P<page>\d+)/$',reports_list),
    ('^feedback/$',reports_list),

    ('^send_question/$',send_question),
    ('^send_report/$',send_report),




)