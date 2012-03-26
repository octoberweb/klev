# -*- coding: utf-8 -*-
import os
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
try:
    from PIL import Image
except ImportError:
    import Image
import md5
from datetime import datetime, date, timedelta

from apps.utils.context_processors import custom_proc
from apps.products.models import Section, Category, Product, SubCategory



def catalog_view(request, section_alias=None, category_alias=None):
    try:
        section = Section.items.get(alias=section_alias)
    except Section.DoesNotExist:
        return HttpResponseRedirect(u'/')

    categories = section.get_categories()

    category = False
    if category_alias:
        try:
            category = Category.items.select_related().get(alias=category_alias)
        except Category.DoesNotExist:
            return HttpResponseRedirect(u'/')


    if category_alias:
        products = Product.items.filter(subcategory__category=category)
    else:
        products = Product.items.filter(subcategory__category__section=section)

    sale_products = products.exclude(old_price__isnull=True)

    products_count = products.count()
    return render_to_response(
        'products/catalog.html',
        {
            'section':section,
            'category':category,
            'category_alias':category_alias,
            'categories':categories,
            'section_alias':section.alias,
            'products':products,
            'sale_products':sale_products[:2],
            'products_count':products_count
            #'menu_url': u'/countries/'
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )


def product_view(request, product_id=None):
    if not product_id:
        return  HttpResponseRedirect(u'/')

    product_id = int(product_id)

    try:
        product = Product.items.select_related().get(id=product_id)
    except Product.DoesNotExist:
        return  HttpResponseRedirect(u'')

    subcategory = product.subcategory
    category = subcategory.category
    section = category.section
    categories = section.get_categories()

    similar_products = Product.items.filter(subcategory=subcategory).exclude(id=product_id)
    similar_products = similar_products.order_by("?")[:4]

    params = product.get_params()
    return render_to_response(
        'products/catalog_item.html',
        {
            'section':section,
            'category':category,
            'category_alias':category.alias,
            'categories':categories,
            'section_alias':section.alias,
            'similar_products':similar_products,
            'product':product,
            'params':params
            #'menu_url': u'/countries/'
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )




