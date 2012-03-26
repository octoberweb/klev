# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from sorl.thumbnail.admin import AdminImageMixin
from django.http import HttpResponse
from apps.orders.models import Cart, CartProduct



class CartProductInlines(admin.TabularInline):
    model = CartProduct
    readonly_fields = ('product',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','create_date', 'user', 'sessionid')
    list_display_links = ('id','create_date',)
    ordering = ('-create_date',)
    list_filter = ('create_date',)
    inlines = [CartProductInlines]

admin.site.register(Cart, CartAdmin)


'''

def set_status_new(modeladmin, request, queryset):
    if request.user.is_staff:
        queryset.update(state = u'new')
    else:
        return HttpResponse('403 Forbidden. Authentication Required!')
set_status_new.short_description = u'Установить статус "Новый"'

def set_status_work(modeladmin, request, queryset):
    if request.user.is_staff:
        queryset.update(state = u'work')
    else:
        return HttpResponse('403 Forbidden. Authentication Required!')
set_status_work.short_description = u'Установить статус "В обработке"'

def set_status_done(modeladmin, request, queryset):
    if request.user.is_staff:
        queryset.update(state = u'done')
    else:
        return HttpResponse('403 Forbidden. Authentication Required!')
set_status_done.short_description = u'Установить статус "Выполнен"'



class OrderPersonalPhotoInlines(AdminImageMixin, admin.TabularInline):
    readonly_fields = ('personal_photo',)
    model = OrderPersonalPhoto

class OrderStockPhotoInlines(AdminImageMixin, admin.TabularInline):
    readonly_fields = ('stock_photo',)
    model = OrderStockPhoto

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','create_date', 'user', 'name','telephone', 'admin_total_summary', 'state',)
    list_display_links = ('id','create_date',)
    search_fields = ('name','telephone','comment')
    ordering = ('-create_date',)
    list_filter = ('create_date','state',)
    inlines = [OrderPersonalPhotoInlines,OrderStockPhotoInlines]
    filter_horizontal = ('collage_personal',)
    readonly_fields = ('create_date', 'user','name','telephone','comment',)
    actions = [set_status_new, set_status_work, set_status_done]
    exclude = ('personal_photos','stock_photos','collage_personal',)

admin.site.register(Order, OrderAdmin)



class CollagePersonalAdmin(AdminImageMixin,admin.ModelAdmin):
    list_display = ('id','create_date',)
    list_display_links = ('id','create_date',)
    filter_horizontal = ('personal_photo',)

admin.site.register(CollagePersonal,CollagePersonalAdmin)
'''