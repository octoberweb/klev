# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from apps.utils.widgets import Redactor
from sorl.thumbnail.admin import AdminImageMixin

from apps.news.models import News

#--Виджеты jquery Редактора
class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=Redactor(attrs={'cols': 100, 'rows': 10},))
    description.label=u'Описание'

    full_description = forms.CharField(widget=Redactor(attrs={'cols': 100, 'rows': 10},), required=False)
    full_description.label=u'Полное описание'

    class Meta:
        model = News
#--Виджеты jquery Редактора

class NewsAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','pub_date','header','has_full', 'show',)
    list_display_links = ('id','pub_date','header',)
    list_editable = ('has_full', 'show',)
    list_filter = ('pub_date','has_full', 'show',)
    search_fields = ('header', 'description','full_description',)
    form = NewsAdminForm

admin.site.register(News, NewsAdmin)