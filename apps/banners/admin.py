from django.contrib import admin
from apps.banners.models import Banners


class BannersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'banner_width', 'banner_height','flash', 'show', )
    list_display_links = ('id', 'name', )

admin.site.register(Banners, BannersAdmin)