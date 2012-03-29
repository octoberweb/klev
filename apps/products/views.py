# -*- coding: utf-8 -*-
import os
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
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
        if key not in ['storage','subcategory','sort']:
            key_value = getvars[key]
            try:
                property = Property.objects.get(alias=key)
            except Property.DoesNotExist:
                continue
            products_id = Param.objects.select_related().filter(product__in=products).filter(property=property).filter(value=key_value).values_list('product',flat=True)
            products = products.filter(id__in=products_id)


    if 'sort' in getvars:
        sort = getvars['sort']

        if sort == u'asc':
            sort = u'price'
        elif sort == u'desc':
            sort = u'-price'
        elif sort not in [u'asc',u'desc']:
            sort = u'price'

        products = products.order_by(sort)

    if 'top_sale' in getvars:
        top_sale = getvars['top_sale']
        if top_sale == u'all':
            products = products.filter(top=True)

    if 'recomended_sale' in getvars:
        recomended_sale = getvars['recomended_sale']
        if recomended_sale == u'all':
            products = products.filter(recomended=True)

    sale_products = all_products.exclude(old_price__isnull=True)[:3]
    top_products = all_products.filter(top=True)[:3]
    recomended_products = all_products.filter(recomended=True)[:3]

    products_count = products.count()

    all = False
    if 'all' in getvars:
        all = getvars['all']
        if all != u'all':
            all = False
        else:
            if products_count > 150:
                all = False



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
            'sale_products':sale_products,
            'top_products':top_products,
            'recomended_products':recomended_products,
            'products_count':products_count,
            'subcategories':subcategories,
            'storages':storages,
            'properties':properties,
            'all':all

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
        return  HttpResponseRedirect(u'/')

    subcategory = product.subcategory
    if not subcategory.show:
        return  HttpResponseRedirect(u'/')

    category = subcategory.category
    if not category.show:
        return  HttpResponseRedirect(u'/')

    section = category.section
    if not section.show:
        return  HttpResponseRedirect(u'/')

    categories = section.get_categories()

    subcategories = category.get_subcategories()

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
            'subcategories':subcategories,
            'section_alias':section.alias,
            'similar_products':similar_products,
            'product':product,
            'params':params
            #'menu_url': u'/countries/'
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )




def search_view(request):
    if 'q' not in request.GET:
        return HttpResponseRedirect('/')
    else:
        q = request.GET['q']
        q = q.strip()

        products = Product.items.distinct().filter(
            Q(name__icontains=q)|
            Q(description__icontains=q)|
            Q(keywords__icontains=q)|
            Q(subcategory__name__icontains=q)
        )

        storages_id = products.distinct().values_list('storage')
        storages = Storage.items.filter(id__in=storages_id).exclude(name=u'Товары в пути')

        getvars = request.GET.copy()
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


        products_count = products.count()
        return render_to_response(
            'products/search.html',
            {
                'products':products,
                'products_count':products_count,
                'storages':storages
            },
            context_instance=RequestContext(request, processors=[custom_proc])
        )

@csrf_exempt
def get_categories(request):
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    else:
        if 'section_alias' not in request.GET:
            return HttpResponseBadRequest()

        section_alias = request.GET['section_alias']
        try:
            section = Section.items.get(alias=section_alias)
        except Section.DoesNotExist:
            return HttpResponseBadRequest()

        categories = section.get_categories()

        categories_html = render_to_string(
            'products/submenu_categories.html',
            {
                'categories':categories,
                'category_alias':None

            }
        )

        return HttpResponse(categories_html)


@csrf_exempt
def get_products(request):
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    else:
        if 'type_el' not in request.GET:
            return HttpResponseBadRequest()

        type_el = request.GET['type_el']

        if type_el not in [u'sale',u'top',u'recomended']:
            return HttpResponseBadRequest()

        if type_el == u'sale':
            products = Product.items.exclude(old_price__isnull=True)
            products = products.order_by('?')
        if type_el == u'top':
            products = Product.items.filter(top=True)
            products = products.order_by('?')
        if type_el == u'recomended':
            products = Product.items.filter(recomended=True)
            products = products.order_by('?')

        products = products[:12]
        product_items = render_to_string(
            'products/product_items.html',
            {
                'sale_products':products
            }
        )

        return HttpResponse(product_items)


