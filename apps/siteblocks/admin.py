# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.siteblocks.models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id','name','url','order',)
    list_display_links = ('id','name',)
    ordering = ('-order',)
    list_editable = ('url', 'order',)

admin.site.register(Menu, MenuAdmin)

