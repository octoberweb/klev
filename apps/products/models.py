# -*- coding: utf-8 -*-
import os, datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from pytils.translit import translify
from sorl.thumbnail import ImageField

from apps.utils.managers import VisibleObjects

def file_path_Category(instance, filename):
    return os.path.join('images','category',  translify(filename).replace(' ', '_') )
class Category(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=100)
    alias = models.CharField(verbose_name=u'Название En', max_length=100, unique=True)
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Category)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name =_(u'category')
        verbose_name_plural =_(u'categories')
        ordering = ['-order', 'name']

    def __unicode__(self):
        return self.name

    #def get_absolute_url(self):
    #    return u'/countries/%s/' %self.alias

    def get_subcategories(self):
        return self.subcategory_set.filter(show=True)

class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'Категория')
    name = models.CharField(verbose_name=u'Название', max_length=100)
    alias = models.CharField(verbose_name=u'Название En', max_length=100, unique=True)
    #image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Category)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name = _(u'subcategory')
        verbose_name_plural = _(u'subcategories')
        ordering = ['-order', 'name']

    def __unicode__(self):
        return self.name

    #def get_absolute_url(self):
    #    return u'/countries/%s/' %self.alias

    def get_products(self):
        return self.product_set.filter(show=True)

def file_path_Brand(instance, filename):
    return os.path.join('images','brand',  translify(filename).replace(' ', '_') )
class Brand(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=100)
    alias = models.CharField(verbose_name=u'Название En', max_length=100, unique=True)
    description = models.TextField(verbose_name=u'Описание')
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Category)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name =_(u'brand')
        verbose_name_plural =_(u'brands')
        ordering = ['-order', 'name']

    def __unicode__(self):
        return self.name

    #def get_absolute_url(self):
    #    return u'/countries/%s/' %self.alias




class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, verbose_name=u'Подкатегория')
    name = models.CharField(verbose_name=u'Название', max_length=100)
    description = models.TextField(verbose_name=u'Описание')
    #full_description = models.TextField(verbose_name=u'Полное описание')
    #alias = models.CharField(verbose_name=u'Название En', max_length=100, unique=True)
    #image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Category)
    price = models.IntegerField(verbose_name=u'Цена')
    recomended = models.BooleanField(verbose_name=u'Рекомендован', default=False)
    keywords = models.CharField(max_length=100, verbose_name=u'Ключевые слова', blank=True)


    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name =_(u'product_item')
        verbose_name_plural =_(u'product_items')
        ordering = ['-order', 'name']

    def __unicode__(self):
        return self.name