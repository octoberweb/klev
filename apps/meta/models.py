# -*- coding: utf-8 -*-
from django.db import models

class Meta(models.Model):
    url = models.CharField(max_length = 100, verbose_name = u'Адрес')
    description = models.CharField(max_length = 100, verbose_name = u'Description',blank=True)
    keywords = models.CharField(max_length = 100, verbose_name = u'Keywords',blank=True)
    title = models.CharField(max_length = 100, verbose_name = u'Заголовок')

    class Meta:
        verbose_name = u'META'
        verbose_name_plural = u'META'

    def __unicode__(self):
        return u'%s -> %s' % (self.title, self.url)
