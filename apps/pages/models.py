# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=120, verbose_name=u'Заголовок страницы', blank=True)
    url = models.CharField(max_length=200, verbose_name=u'Адрес', unique=True, help_text=u'Адрес страницы на латинице. (/your_address/)')
    content = models.TextField(verbose_name=u'Содержимое страницы', blank=True)
    is_published = models.BooleanField(default=True, verbose_name=u'Публиковать страницу')


    class Meta:
        verbose_name = _(u'page_item')
        verbose_name_plural = _(u'page_items')

    def __unicode__(self):
        return self.title

  