# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from pytils.translit import translify
import os

from apps.utils.managers import VisibleObjects


def file_path(instance, filename):
    return os.path.join('images', 'banners', translify(filename).replace(' ', '_') )

class Banners(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Название')
    banner_file = models.FileField(upload_to=file_path, verbose_name=u'Файл')
    href = models.URLField(verbose_name=u'Ссылка', blank=True)
    banner_width = models.CharField(max_length=4,verbose_name=u'Ширина', help_text=u'Ширина баннера справа: 150px. Ширина нижнего баннера: 500px.')
    banner_height = models.CharField(max_length=4, verbose_name=u'Высота', help_text=u'Высота баннера справа: 220px. Высота нижнего баннера: 72px.')

    #left = models.BooleanField(verbose_name=u'Баннер под меню', default=False)
    #right = models.BooleanField(verbose_name=u'Баннер на главной справа', default=False)
    flash = models.BooleanField(verbose_name=u'Flash', default=False)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)
    order = models.IntegerField(verbose_name=u'Порядок',max_length=3, default=10)

    objects = models.Manager() # The default manager.
    items = VisibleObjects() # The visible objects manager.

    class Meta:
        verbose_name = _(u'banner_item')
        verbose_name_plural = _(u'banner_items')

    def get_src_file(self):
        return self.banner_file.url

    def __unicode__(self):
        return self.name
