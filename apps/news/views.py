# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import loader, RequestContext, Context
from django.http import *

from apps.utils.context_processors import custom_proc
from apps.news.models import News



def news_list(request):
    news = News.items.all()

    return render_to_response(
        'news_events/news.html',
        {
            'news':news,
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )



def news_detail(request, news_id):
    try:
        news_item = News.objects.get(id=news_id)
    except News.DoesNotExist:
        raise Http404()

    if not news_item.show:
        raise Http404()

    return render_to_response(
            'news_events/new.html',
            {'new':news_item
             },
            context_instance=RequestContext(request, processors=[custom_proc])
        )