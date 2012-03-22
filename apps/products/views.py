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



def section_view(request, section_alias=None):
    try:
        section = Section.objects.get(alias=section_alias)
    except Section.DoesNotExist:
        return HttpResponseRedirect(u'/')

    if not section.show:
        return HttpResponseRedirect(u'/')

    categories = section.get_categories()




    return render_to_response(
        'products/catalog.html',
        {
            'section':section,
            'categories':categories,
            'section_alias':section.alias
            #'menu_url': u'/countries/'
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )