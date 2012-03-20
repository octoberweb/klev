# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.pages.models import Page
from apps.utils.widgets import Redactor


#--Виджеты jquery Редактора
class ModelAdminForm(forms.ModelForm):
    content = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 30}), required=False)
    content.label=u'Содержание'

    class Meta:
        model = Page
#--Виджеты jquery Редактора


class PageAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'url', 'is_published',)
    list_display_links = ('id', 'title', 'url',)
    search_fields = ('title', 'url','content',)
    list_editable = ('is_published',)
    form = ModelAdminForm


admin.site.register(Page, PageAdmin)
  