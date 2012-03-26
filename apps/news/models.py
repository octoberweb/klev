# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from pytils.translit import translify
import datetime, os

from apps.utils.managers import VisibleObjects
from sorl.thumbnail import ImageField

def file_path_News(instance, filename):
    return os.path.join('images','news',  translify(filename).replace(' ', '_') )
class News(models.Model):
    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'Дата')
    header = models.CharField(max_length=300, verbose_name=u'Заголовок')
    description = models.TextField(verbose_name=u'Описание')
    has_full = models.BooleanField(verbose_name=u'Есть полное описание', default=False)
    full_description = models.TextField(verbose_name=u'Полное описание', blank=True)

    image = ImageField(verbose_name=u'Картинка',upload_to=file_path_News)

    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.
    
    def get_absolute_url(self):
        return "/news/%i/" % self.id

    class Meta:
        verbose_name =_(u'news_item')
        verbose_name_plural =_(u'news_items')
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.header