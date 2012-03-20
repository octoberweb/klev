# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from pytils.translit import translify

import os, datetime


class Menu(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Заголовок')
    url = models.CharField(max_length=50, verbose_name=u'Адрес', unique=True)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    show = models.BooleanField(verbose_name=u'Отображать', default=True)

    class Meta:
        verbose_name =_(u'menu_item')
        verbose_name_plural =_(u'menu_items')
        ordering = ['-order']

    def __unicode__(self):
        return self.name
