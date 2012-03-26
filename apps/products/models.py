# -*- coding: utf-8 -*-
import os, datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from pytils.translit import translify
from sorl.thumbnail import ImageField

from apps.utils.managers import VisibleObjects

class Property(models.Model):
    xml_id = models.CharField(verbose_name=u'Идентификатор', max_length=100, blank=True)
    name = models.CharField(verbose_name=u'Наименование', max_length=400)

    class Meta:
        verbose_name =_(u'property')
        verbose_name_plural =_(u'properties')

    def __unicode__(self):
        return u'%s, %s ' %(self.xml_id, self.name)

def file_path_Section(instance, filename):
    return os.path.join('images','section',  translify(filename).replace(' ', '_') )
class Section(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=100)
    alias = models.CharField(verbose_name=u'Алиас', max_length=100, unique=True)
    xml_name = models.CharField(verbose_name=u'Название в xml', max_length=100, unique=True)
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Section, blank=True)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name =_(u'section')
        verbose_name_plural =_(u'sections')
        ordering = ['-order', 'name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u'/section/%s/' %self.alias
        #return u'/section/%s/' %self.xml_name


    def get_categories(self):
        return self.category_set.filter(show=True)




class Category(models.Model):
    section = models.ForeignKey(Section, verbose_name=u'Раздел (Класс товара)')
    name = models.CharField(verbose_name=u'Название', max_length=100)
    alias = models.CharField(verbose_name=u'Алиас', max_length=100, unique=True)
    xml_name = models.CharField(verbose_name=u'Название в xml', max_length=100, unique=True)
    #image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Category)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name =_(u'category')
        verbose_name_plural =_(u'categories')
        ordering = ['-order', 'name']

    def __unicode__(self):
        return u'%s | %s' %(self.section.name, self.name)

    def get_absolute_url(self):
        return u'%s%s/' %(self.section.get_absolute_url(),self.alias)

    def get_subcategories(self):
        return self.subcategory_set.filter(show=True)

class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'Категория (Вид товара)')
    name = models.CharField(verbose_name=u'Название', max_length=100)
    alias = models.CharField(verbose_name=u'Алиас', max_length=100, unique=True)
    xml_name = models.CharField(verbose_name=u'Название в xml', max_length=100, unique=True)
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
        return u'%s | %s' %(self.category.name, self.name)

    #def get_absolute_url(self):
    #    return u'/countries/%s/' %self.alias

    def get_products(self):
        return self.product_set.filter(show=True)

class Storage(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=100)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name =_(u'storage')
        verbose_name_plural =_(u'storages')
        ordering = ['name']

    def __unicode__(self):
        return self.name

def file_path_Product(instance, filename):
    return os.path.join('images','product',  translify(filename).replace(' ', '_') )
class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, verbose_name=u'Подкатегория')
    name = models.CharField(verbose_name=u'Название', max_length=100)
    xml_id = models.CharField(verbose_name=u'ID в xml', max_length=100, unique=True)
    description = models.TextField(verbose_name=u'Описание', blank=True)
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Product,blank=True)
    keywords = models.CharField(max_length=400, verbose_name=u'Ключевые слова')
    price = models.DecimalField(verbose_name=u'Цена', decimal_places=2, max_digits=10, blank=True, null=True)
    old_price = models.DecimalField(verbose_name=u'Старая цена', decimal_places=2, max_digits=10, blank=True, null=True)
    recomended = models.BooleanField(verbose_name=u'Рекомендован', default=False)

    storage = models.ForeignKey(Storage, verbose_name=u'Склад',blank=True, null=True)
    top = models.BooleanField(verbose_name=u'Лидер', default=False)

    count = models.IntegerField(verbose_name=u'Остаток', default=0, blank=True)

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

    def get_absolute_url(self):
        return u'/product/%d/' %self.id

    def get_price(self):
        price = self.price
        value = u'%s' %price
        if price._isinteger():
            value = u'%s' %value[:len(value)-3]
            count = 3
        else:
            count = 6

        if len(value)>count:
            ends = value[len(value)-count:]
            starts = value[:len(value)-count]

            return u'%s %s' %(starts, ends)
        else:
            return value

    def get_old_price(self):
        price = self.old_price
        value = u'%s' %price
        if price._isinteger():
            value = u'%s' %value[:len(value)-3]
            count = 3
        else:
            count = 6

        if len(value)>count:
            ends = value[len(value)-count:]
            starts = value[:len(value)-count]

            return u'%s %s' %(starts, ends)
        else:
            return value

    def get_params(self):
        return self.param_set.select_related().all()


class Param(models.Model):
    product = models.ForeignKey(Product)
    property = models.ForeignKey(Property, verbose_name=u'Свойство')
    value = models.TextField(verbose_name=u'Значение')

    class Meta:
        verbose_name =_(u'param')
        verbose_name_plural =_(u'params')

    def __unicode__(self):
        return u'%s: %s' %(self.property.name, self.value)
