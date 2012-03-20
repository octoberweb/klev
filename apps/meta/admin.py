# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.meta.models import Meta

class MetaAdmin(admin.ModelAdmin):
    list_display = ('url','title',)
    list_display_links = ('url','title',)
    search_fields = ('url','title',)

admin.site.register(Meta, MetaAdmin)
