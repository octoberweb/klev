# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor

from apps.products.models import Section, Property, Category, SubCategory,Product, Param
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

class PropertyAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','xml_id','name',)
    list_display_links = ('id','xml_id',)
    search_fields = ('xml_id','name',)

admin.site.register(Property, PropertyAdmin)


class CategoryInline(admin.TabularInline):
    model = Category

class SectionAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','name','alias','xml_name', 'order','show',)
    list_display_links = ('id','name',)
    #list_editable = ('order','show','xml_name',)
    list_editable = ('order','show',)
    inlines = [CategoryInline]
    #form = ModelAdminForm

admin.site.register(Section, SectionAdmin)

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
class CategoryAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','name','section','alias','xml_name', 'order','show',)
    list_display_links = ('id','name',)
    list_editable = ('order','show',)
    list_filter = ('section',)
    inlines = [SubCategoryInline]
    #form = ModelAdminForm

admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','name', 'category', 'alias','xml_name', 'order','show',)
    list_display_links = ('id','name',)
    list_editable = ('order','show',)
    list_filter = ('category',)
    #inlines = [CountryPhotoInline,InfoInline]
    #form = ModelAdminForm

admin.site.register(SubCategory, SubCategoryAdmin)

class ParamInline(admin.TabularInline):
    model = Param

class ProductAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','xml_id', 'name', 'subcategory', 'price','old_price','recomended','top', 'order','show',)
    list_display_links = ('id','xml_id','name',)
    list_editable = ('order','show',)
    list_filter = ('show','recomended','top', 'subcategory', )
    search_fields = ['xml_id', 'name','subcategory__name', 'keywords' ]
    inlines = [ParamInline]
    #form = ModelAdminForm

admin.site.register(Product, ProductAdmin)