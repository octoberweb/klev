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
    alias = models.CharField(verbose_name=u'Алиас', max_length=400)


    class Meta:
        verbose_name =_(u'property')
        verbose_name_plural =_(u'properties')

    def __unicode__(self):
        return u'%s, %s ' %(self.xml_id, self.name)

    def get_values(self, products):
        return self.param_set.distinct().select_related().filter(product__in=products)


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

    def get_absolute_url(self):
        return u'%s?subcategory=%s' %(self.category.get_absolute_url(), self.id)

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

    def get_absolute_url(self):
            return u'?storage=%d' %self.id

def file_path_Brand(instance, filename):
    return os.path.join('images','brands',  translify(filename).replace(' ', '_') )
class Brand(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=100)
    alias = models.CharField(verbose_name=u'Алиас', max_length=100, unique=True)
    xml_name = models.CharField(verbose_name=u'Название в xml', max_length=100, unique=True)
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Brand, blank=True)
    description = models.TextField(verbose_name=u'Описание', blank=True)

    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name = _(u'brand')
        verbose_name_plural = _(u'brands')
        ordering = ['-order', 'name']

    def __unicode__(self):
        return self.name

    def get_products(self):
        return self.product_set.filter(show=True)


def file_path_Product(instance, filename):
    return os.path.join('images','products',  translify(filename).replace(' ', '_') )
class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, verbose_name=u'Подкатегория')
    brand = models.ForeignKey(Brand, verbose_name=u'Бренд', blank=True, null=True)
    name = models.CharField(verbose_name=u'Название', max_length=400)
    xml_id = models.CharField(verbose_name=u'ID в xml', max_length=100, unique=True)
    description = models.TextField(verbose_name=u'Описание', blank=True)
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Product,blank=True)
    keywords = models.TextField(verbose_name=u'Ключевые слова')
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
        return u'ID:%s, XML_ID:%s, %s' %(self.id, self.xml_id, self.name)

    def get_absolute_url(self):
        return u'/product/%d/' %self.id

    def get_price(self):
        price = self.price
        if not price:
            return u'-----'
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

    def get_photos(self):
            return self.photo_set.all()

class Param(models.Model):
    product = models.ForeignKey(Product)
    property = models.ForeignKey(Property, verbose_name=u'Свойство')
    value = models.TextField(verbose_name=u'Значение')

    class Meta:
        verbose_name =_(u'param')
        verbose_name_plural =_(u'params')

    def __unicode__(self):
        return u'%s: %s' %(self.property.name, self.value)



def file_path_Product(instance, filename):
     return os.path.join('images','products',  translify(filename).replace(' ', '_') )
class Photo(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Товар')
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Product)

    class Meta:
        verbose_name =_(u'photo')
        verbose_name_plural =_(u'photos')

    def __unicode__(self):
        return u'Фото товара %s' %self.product.name



def file_path_ImportXML(instance, filename):
     return os.path.join('xml_files',translify(filename).replace(' ', '_') )
class ImportXML(models.Model):
    pub_date = models.DateTimeField(verbose_name=u'Дата загрузки', default=datetime.datetime.now)
    file = models.FileField(verbose_name=u'XML файл', upload_to=file_path_ImportXML)

    class Meta:
        verbose_name = u'Импорт XML'
        verbose_name_plural = u'Импорты XML'

    def __unicode__(self):
        return u'Импорт от %s' %self.pub_date

from django.db.models.signals import post_save
import os
from xml.etree import ElementTree as ET
#from apps.products.models import Property, Product, Section, Category, SubCategory, Param,Storage, Brand
from decimal import Decimal, InvalidOperation
from pytils.translit import translify
from django.http import HttpResponse

def upload_xml(sender, instance, created, **kwargs):
    if created:
        file = instance.file
        if file:
            file_path = file.path
            try:
                doc = ET.parse(file_path)
            except IOError:
                return HttpResponse(u'nofile')

            root = doc.getroot()
            calalog = root.find(u'Каталог')
            if len(calalog):
                properties = calalog.findall(u'Свойство')

                for pr in properties:
                    try:
                        prop_ID = unicode(pr.attrib[u'Идентификатор']).strip()
                    except KeyError:
                        #prop_ID = False
                        continue

                    prop_name = unicode(pr.attrib[u'Наименование']).strip()

                    if prop_ID:
                        try:
                            prop = Property.objects.get(xml_id=prop_ID)
                        except Property.DoesNotExist:
                            prop_alias = prop_name.replace(',','').replace(' ','_').lower()
                            prop_alias = translify(prop_alias)
                            Property.objects.create(
                                xml_id=prop_ID,
                                name=prop_name,
                                alias=prop_alias
                            )

                products = calalog.findall(u'Товар')

                for prod in products:
                    try:
                        prod_ID = unicode(prod.attrib[u'Идентификатор']).strip()
                    except KeyError:
                        #prop_ID = False
                        continue
                    values_prop = prod.findall(u'ЗначениеСвойства')

                    section_value = False
                    category_value = False
                    subcategory_value = False
                    product_name = False
                    product_brand = False

                    prop_list = []
                    for value_prop in values_prop:
                        prop_ID = unicode(value_prop.attrib[u'ИдентификаторСвойства']).strip()
                        try:
                            value = unicode(value_prop.attrib[u'Значение']).strip()
                        except KeyError:
                            continue
                        if prop_ID == u'00003': #Вид товара (Категория)
                            category_value = value
                        elif prop_ID == u'Ц0070': #Класс товара (Раздел)
                            section_value = value
                        elif prop_ID == u'Ц0077': #Подвид товара (Подкатегория)
                            subcategory_value = value
                        elif prop_ID == u'ПолноеНаименование': #Подвид товара (Подкатегория)
                            product_name = value
                        elif prop_ID == u'Ц0076': #Бренд
                            product_brand = value
                        elif prop_ID == u'КЕ002': #Старая цена
                            continue
                        else:
                            prop_list.append([prop_ID, value])

                    if not section_value or not category_value or not subcategory_value or not product_name:
                        continue

                    try:
                        product = Product.objects.get(xml_id=prod_ID)
                    except Product.DoesNotExist:
                        try:
                            section = Section.objects.select_related().get(xml_name=section_value)
                        except Section.DoesNotExist:
                            section = Section.objects.select_related().create(
                                name=section_value,
                                alias=section_value.replace(u' ', u'_').replace(u',', u''),
                                xml_name=section_value
                            )
                        try:
                            category = Category.objects.select_related().get(xml_name=category_value)
                        except Category.DoesNotExist:
                            category = Category.objects.select_related().create(
                                section=section,
                                name=category_value,
                                alias=category_value.replace(u' ', u'_').replace(u',', u''),
                                xml_name=category_value
                            )

                        try:
                            subcategory = SubCategory.objects.select_related().get(xml_name=subcategory_value)
                        except SubCategory.DoesNotExist:
                            subcategory = SubCategory.objects.select_related().create(
                                category=category,
                                name=subcategory_value,
                                alias=subcategory_value.replace(u' ', u'_').replace(u',', u''),
                                xml_name=subcategory_value
                            )
                        keywords = u'%s %s' % (product_name, subcategory.name)

                        if product_brand:
                            try:
                                brand = Brand.objects.get(xml_name=product_brand)
                            except Brand.DoesNotExist:
                                brand = Brand.objects.create(
                                    name=product_brand,
                                    alias=product_brand.replace(u' ', u'_').replace(u',', u''),
                                    xml_name=product_brand
                                )
                        else:
                            brand = None
                        product = Product.objects.create(
                            subcategory=subcategory,
                            brand=brand,
                            name=product_name,
                            xml_id=prod_ID,
                            keywords=keywords
                        )

                        if prop_list:
                            for p in prop_list:
                                try:
                                    property = Property.objects.get(xml_id=p[0])
                                except Property.DoesNotExist:
                                    continue

                                Param.objects.create(
                                    product=product,
                                    property=property,
                                    value=p[1]
                                )

            package = root.find(u'ПакетПредложений')
            if len(package):
                proposals = package.findall(u'Предложение')

                for proposal in proposals:
                    try:
                        product_xml_id = unicode(proposal.attrib[u'ИдентификаторТовара']).strip()
                        product_count = unicode(proposal.attrib[u'Количество']).strip()
                        product_price = unicode(proposal.attrib[u'Цена']).strip()
                    except KeyError:
                        continue

                    try:
                        product_old_price = unicode(proposal.attrib[u'СтараяЦена']).strip()
                    except KeyError:
                        product_old_price = None

                    try:
                        product = Product.objects.get(xml_id=product_xml_id)
                    except Product.DoesNotExist:
                        continue


                    presence = proposal.find(u'Наличие')

                    try:
                        storage_xml = unicode(presence.attrib[u'Склад']).strip()
                    except (KeyError, AttributeError):
                        continue

                    try:
                        storage = Storage.objects.get(name=storage_xml)
                    except Storage.DoesNotExist:
                        storage = Storage.objects.create(
                            name=storage_xml,
                            show=False
                        )


                    product_price = Decimal(product_price).quantize(Decimal(10) ** -2)
                    product.price = product_price
                    if product_old_price:
                        product_old_price = Decimal(product_old_price).quantize(Decimal(10) ** -2)
                        product.old_price = product_old_price
                    else:
                        product.old_price = product_old_price

                    product.storage = storage
                    product.count = product_count
                    try:
                        product.save()
                    except ValueError:
                        continue


post_save.connect(upload_xml, sender=ImportXML)



