# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from apps.utils.widgets import Redactor
from sorl.thumbnail.admin import AdminImageMixin

from apps.news.models import News, Event

#--Виджеты jquery Редактора
class NewsAdminForm(forms.ModelForm):
    full_description = forms.CharField(widget=Redactor(attrs={'cols': 100, 'rows': 10},), required=False)
    full_description.label=u'Полное описание'

    class Meta:
        model = News
#--Виджеты jquery Редактора

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','pub_date','header','show',)
    list_display_links = ('id','pub_date','header',)
    list_editable = ('show',)
    search_fields = ('header', 'description','full_description',)
    ordering = ('-pub_date',)
    form = NewsAdminForm

admin.site.register(News, NewsAdmin)


#--Виджеты jquery Редактора
class EventAdminForm(forms.ModelForm):
    full_description = forms.CharField(widget=Redactor(attrs={'cols': 100, 'rows': 10},), required=False)
    full_description.label=u'Полное описание'

    class Meta:
        model = Event
#--Виджеты jquery Редактора

class EventAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','name','digits','month','order','show',)
    list_display_links = ('id','name',)
    list_editable = ('digits','month','order', 'show',)
    search_fields = ('name', 'description','full_description','month','digits',)
    ordering = ('-order',)
    form = EventAdminForm

admin.site.register(Event, EventAdmin)