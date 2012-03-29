# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from pytils.translit import translify
import datetime, os
from django.contrib.auth.models import User

from apps.products.models import Brand, Product

class Distributor(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь', unique=True)
    brand = models.ManyToManyField(Brand, verbose_name=u'Бренды')
    
    class Meta:
        verbose_name =_(u'distributor')
        verbose_name_plural =_(u'distributor')
        ordering = ('user',)

    def __unicode__(self):
        return self.user

    def get_brands(self):
        return self.brand.all()

    def get_products(self):
        brands = self.get_brands()
        products = Product.items.filter(brand__in=brands)
        return products