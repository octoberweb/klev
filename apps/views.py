# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import loader, RequestContext, Context
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from apps.utils.context_processors import custom_proc
from django.conf import settings

from apps.products.models import Product, Section

def index(request):

    all_products = Product.items.all()
    sections = Section.items.all()

    sale_products = all_products.exclude(old_price__isnull=True)
    sale_products_count = sale_products.count()
    sections_id = sale_products.values_list('subcategory__category__section', flat=True)
    sale_sections = sections.filter(id__in=sections_id)
    sale_products = sale_products.order_by('?')[:12]

    top_products = all_products.filter(top=True)
    top_products_count = top_products.count()
    sections_id = top_products.values_list('subcategory__category__section', flat=True)
    top_sections = sections.filter(id__in=sections_id)

    recomended_products = all_products.filter(recomended=True)
    recomended_products_count = recomended_products.count()
    sections_id = recomended_products.values_list('subcategory__category__section', flat=True)
    recomended_sections = sections.filter(id__in=sections_id)



    return render_to_response(
        'index.html',
        {
            'sale_products':sale_products,
            'sale_products_count':sale_products_count,
            'sale_sections':sale_sections,
            'top_sections':top_sections,
            'top_products_count':top_products_count,
            'recomended_sections':recomended_sections,
            'recomended_products_count':recomended_products_count


        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )
