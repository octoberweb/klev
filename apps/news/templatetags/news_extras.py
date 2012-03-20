# -*- coding: utf-8 -*-
from news.models import News
from django import template

register = template.Library()

@register.inclusion_tag("news_last.html")
def get_news_last():
    news = News.objects.order_by('-pub_date')
    if news.count() >3:
        return {'news': news[:3]}
    else:
        return {'news': news}
