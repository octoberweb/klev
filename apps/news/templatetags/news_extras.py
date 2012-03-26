# -*- coding: utf-8 -*-
from apps.news.models import News
from django import template

register = template.Library()

@register.inclusion_tag("news/last_news.html")
def get_last_news():
    news = News.items.all()
    return {'news': news[:3]}
