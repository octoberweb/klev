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
from apps.products.models import Section, Category, Product, SubCategory, Storage, Param, Property



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

    subcategories = False
    properties = False
    if category_alias:
        products = Product.items.select_related().filter(subcategory__category=category)
        subcategories_id = products.distinct().values_list('subcategory')
        subcategories = SubCategory.items.select_related().filter(id__in=subcategories_id)

        #properties_id = Param.objects.distinct().filter(product__in=products).values_list('property',flat=True)
        #properties = Property.objects.distinct().filter(id__in=properties_id)


    else:
        products = Product.items.select_related().filter(subcategory__category__section=section)

    storages_id = products.distinct().values_list('storage')
    storages = Storage.items.filter(id__in=storages_id).exclude(name=u'Товары в пути')

    getvars = request.GET.copy()
    subcategory = False
    if 'subcategory' in getvars:
        subcategory_id = getvars['subcategory']
        try:
            subcategory_id = int(subcategory_id)
        except ValueError:
            subcategory_id = False

        if subcategory_id:
            try:
                subcategory = SubCategory.items.get(id=subcategory_id)
            except SubCategory.DoesNotExist:
                subcategory = False

            if subcategory:
                products = products.filter(subcategory=subcategory)

                properties_id = Param.objects.distinct().filter(product__in=products).values_list('property',flat=True)
                properties = Property.objects.distinct().filter(id__in=properties_id)


    if 'storage' in getvars:
        storage_id = getvars['storage']
        try:
            storage_id = int(storage_id)
        except ValueError:
            storage_id = False

        if storage_id:
            try:
                storage = Storage.items.get(id=storage_id)
            except Storage.DoesNotExist:
                storage = False

            if storage:
                products = products.filter(storage=storage)

    all_products = products
    keys = getvars.keys()
    for key in keys:
        if key not in ['storage','subcategory']:
            key_value = getvars[key]
            try:
                property = Property.objects.get(alias=key)
            except Property.DoesNotExist:
                continue
            products_id = Param.objects.select_related().filter(product__in=products).filter(property=property).filter(value=key_value).values_list('product',flat=True)
            products = products.filter(id__in=products_id)




    sale_products = products.exclude(old_price__isnull=True)

    products_count = products.count()
    return render_to_response(
        'products/catalog.html',
        {
            'section':section,
            'category':category,
            'category_alias':category_alias,
            'subcategory':subcategory,
            'categories':categories,
            'section_alias':section.alias,
            'products':products,
            'all_products':all_products,
            'sale_products':sale_products[:2],
            'products_count':products_count,
            'subcategories':subcategories,
            'storages':storages,
            'properties':properties

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




