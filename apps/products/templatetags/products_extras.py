# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from string import split

register = template.Library()



@register.inclusion_tag("products/item.html")
def get_product_html(product, product_category='True'):
    if product_category == 'False':
        product_category= False

    return {
        'product': product,
        'product_category':product_category,
    }
