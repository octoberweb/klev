# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from apps.utils.widgets import Redactor

from apps.distributors.models import Distributor


class DistributorAdmin(admin.ModelAdmin):
    list_display = ('id','user',)
    list_display_links = ('id','user',)
    search_fields = ('user__username',)
    filter_horizontal = ('brand',)

admin.site.register(Distributor, DistributorAdmin)