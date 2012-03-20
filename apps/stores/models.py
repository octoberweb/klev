# -*- coding: utf-8 -*-
import os, datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models

from pytils.translit import translify
from sorl.thumbnail import ImageField

from apps.utils.managers import VisibleObjects

def file_path_Store(instance, filename):
    return os.path.join('images','store',  translify(filename).replace(' ', '_') )
class Store(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=100)
    alias = models.CharField(verbose_name=u'Название En', max_length=100, unique=True)
    route = ImageField(verbose_name=u'Схема проезда', upload_to=file_path_Store)
    description = models.TextField(verbose_name=u'Описание')

    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name =_(u'store_item')
        verbose_name_plural =_(u'store_items')
        ordering = ['-order', 'name']

    def __unicode__(self):
        return self.name

    #def get_absolute_url(self):
    #    return u'/countries/%s/' %self.alias

    def get_photos(self):
        return self.photo_set.all()

class Photo(models.Model):
    store = models.ForeignKey(Store, verbose_name=u'Магазин')
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Category)

    class Meta:
        verbose_name =_(u'photo')
        verbose_name_plural =_(u'photos')

    def __unicode__(self):
        return u'Фото магазина %s' %self.store.name