# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor

from apps.stores.models import Store
from sorl.thumbnail.admin import AdminImageMixin
'''
#--Виджеты jquery Редактора
class ModelAdminForm(forms.ModelForm):
    description = forms.CharField(widget=Redactor(attrs={'cols': 170, 'rows': 30}))
    description.label=u'Описание'

    class Meta:
        model = Country
#--Виджеты jquery Редактора

class CountryPhotoInline(AdminImageMixin, admin.TabularInline):
    model = CountryPhoto

class InfoInline(admin.TabularInline):
    model = Info
'''
class StoreAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','name','order','show',)
    list_display_links = ('id','name',)
    list_editable = ('order','show',)
    #inlines = [CountryPhotoInline,InfoInline]
    #form = ModelAdminForm

admin.site.register(Store, StoreAdmin)
