# -*- coding: utf-8 -*-
from django import template
import datetime
from pytils.numeral import choose_plural
from django.db.models import Q

from apps.orders.models import Cart

register = template.Library()


@register.inclusion_tag('orders/cart_block.html')
def get_cart(user, sessionid):
    if user.is_authenticated():
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = False
    else:
        try:
            cart = Cart.objects.get(sessionid=sessionid)
        except Cart.DoesNotExist:
            cart = False

    is_empty = True
    cart_total = 0
    cart_products_count = 0
    cart_products_text = u''
    if cart:
        cart_products_count = cart.get_products_count()
        if cart_products_count:
            cart_total = cart.get_str_total()
            is_empty = False
            cart_products_text = u'товар%s' %(choose_plural(cart_products_count,(u'',u'а',u'ов')))
    return {
        'is_empty':is_empty,
        'cart_products_count':cart_products_count,
        'cart_total':cart_total,
        'cart_products_text':cart_products_text
    }


@register.simple_tag()
def get_sum(cl):
    rl = cl.result_list
    sum = 0
    for order in rl:
        sum += order.get_total_summary()
    return sum