# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from pytils.translit import translify

import os
from sorl.thumbnail import ImageField
import datetime

from apps.products.models import Product



    
class Cart(models.Model):
    create_date = models.DateTimeField(verbose_name=u'Дата создания', default=datetime.datetime.now)
    user = models.ForeignKey(User, verbose_name=u'Пользователь', blank=True, null=True)
    sessionid = models.CharField(max_length=50, verbose_name=u'ID сессии')
    products = models.ManyToManyField(Product, through="CartProduct", blank=True, verbose_name=u'Товары')

    class Meta:
        verbose_name = _(u'cart')
        verbose_name_plural = _(u'carts')

    def __unicode__(self):
        if self.user:
            return self.user.username
        else:
            return self.sessionid

    def get_products(self):
        return CartProduct.objects.select_related().filter(cart=self)
        #return self.products.select_related().all()

    def get_products_count(self):
        return self.get_products().count()


    def get_total(self):
        sum = 0
        for cart_product in self.cartproduct_set.select_related().all():
            sum += cart_product.count * cart_product.product.price
        return sum

    def get_str_total(self):
        total = self.get_total()
        value = u'%s' %total
        if total._isinteger():
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


'''
    def get_products_count(self):
            return CartProduct.objects.filter(cart=self).count()


    def get_total(self):
        sum = 0
        for cart_product in CartProduct.objects.select_related().filter(cart=self):
            sum += cart_product.count * cart_product.product.price
        return sum
'''







class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=u'Корзина')
    count = models.PositiveIntegerField(default=1, verbose_name=u'Количество')
    product = models.ForeignKey(Product, verbose_name=u'Товар')

    class Meta:
        verbose_name =_(u'product_item')
        verbose_name_plural =_(u'product_items')

    def get_total(self):
        total = self.product.price * self.count
        return total

    def get_str_total(self):
        total = self.get_total()
        value = u'%s' %total
        if total._isinteger():
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



from django.db.models.signals import post_save
def delete_old_carts(sender, instance, created, **kwargs):
    if created:
        now = datetime.datetime.now()
        day_ago30 = now - datetime.timedelta(days=30)
        carts = Cart.objects.filter(create_date__lte=day_ago30)
        if carts:
            carts.delete()

post_save.connect(delete_old_carts, sender=CartProduct)

'''


order_choices = (
    (u'new', u'Новый'),
    (u'work', u'В обработке'),
    (u'done', u'Выполнен'),
)

class Order(models.Model):
    create_date = models.DateTimeField(verbose_name=u'Дата создания', default=datetime.datetime.now)
    user = models.ForeignKey(User, verbose_name=u'Пользователь', blank=True, null=True)
    name = models.CharField(verbose_name=u'Имя заказчика',max_length=150)
    telephone = models.CharField(verbose_name=u'Телефон',max_length=100)
    comment = models.TextField(verbose_name=u'Комментарий к заказу')
    personal_photos = models.ManyToManyField(PersonalPhoto, through="OrderPersonalPhoto", related_name="personal_photos_order", blank=True)
    stock_photos = models.ManyToManyField(StockPhoto, through="OrderStockPhoto", related_name="stock_photos_order", blank=True)
    collage_personal = models.ManyToManyField(CollagePersonal, blank=True, verbose_name=u'Коллажи')
    state = models.CharField(verbose_name=u'статус',choices=order_choices, default=u'new', max_length=10)

    class Meta:
        verbose_name = _(u'order')
        verbose_name_plural = _(u'orders')

    def __unicode__(self):
        if self.user:
            return self.user.username
        else:
            return self.name

    def get_stock_photos(self):
        return OrderStockPhoto.objects.filter(order=self)

    def get_personal_photos(self):
        return OrderPersonalPhoto.objects.filter(order=self)

    def get_collage_personal(self):
        return self.collage_personal.all()

    def get_total(self):
        sum = 0
        for cart_stock_photo in OrderStockPhoto.objects.filter(order=self):
            if cart_stock_photo.electronic_form:
                sum += cart_stock_photo.stock_photo.price * cart_stock_photo.count
            else:
                sum += cart_stock_photo.option.price * cart_stock_photo.count

        for cart_personal_photo in OrderPersonalPhoto.objects.filter(order=self):
            if cart_personal_photo.electronic_form:
                sum += cart_personal_photo.personal_photo.price * cart_personal_photo.count
            else:
                sum += cart_personal_photo.option.price * cart_personal_photo.count

        return sum

    def get_total_collage_personal(self):
        sum = 0
        for collage_personal in self.get_collage_personal():
            sum += collage_personal.collage_option.price

        return sum

    def get_total_summary(self):
        return self.get_total() + self.get_total_collage_personal()

    def admin_total_summary(self):
        return '<span>%s</span>' %self.get_total_summary()
    admin_total_summary.allow_tags = True
    admin_total_summary.short_description = 'Сумма'



class OrderPersonalPhoto(models.Model):
    order = models.ForeignKey(Order, verbose_name=u'Заказ')
    count = models.PositiveIntegerField(default=1, verbose_name=u'Количество')
    personal_photo = models.ForeignKey(PersonalPhoto, verbose_name=u'Персональная фотография')
    electronic_form = models.BooleanField(verbose_name=u'в эл.виде', default=False)
    option = models.ForeignKey(Option, blank=True, null=True)

    class Meta:
        verbose_name = u'фотографию'
        verbose_name_plural = u'Персональные фотографии'

    def get_total(self):
        if self.electronic_form:
            return self.personal_photo.price * self.count
        else:
            return self.count * self.option.price
    #def __unicode__(self):
    #    return u'id корзины %s | id товара %s | количество %s' %(self.cart.id, self.product.id, self.count)

class OrderStockPhoto(models.Model):
    order = models.ForeignKey(Order, verbose_name=u'Заказ')
    count = models.PositiveIntegerField(default=1, verbose_name=u'Количество')
    stock_photo = models.ForeignKey(StockPhoto, verbose_name=u'Фотография из фотостока')
    electronic_form = models.BooleanField(verbose_name=u'в эл.виде', default=False)
    option = models.ForeignKey(Option, blank=True, null=True)


    def get_total(self):
        if self.electronic_form:
            return self.stock_photo.price * self.count
        else:
            return self.count * self.option.price

    class Meta:
        verbose_name = u'фотографию'
        verbose_name_plural = u'Фотографии из фотостока''
'''