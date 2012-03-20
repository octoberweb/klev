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
from apps.countries.models import Country


def countries_view(request):
    countries = Country.items.all()

    return render_to_response(
        'countries/countries.html',
        {
            'countries':countries,
            'menu_url': u'/countries/'
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )

def country_view(request, country_alias=None):
    if country_alias is None:
        return HttpResponseRedirect('/countries/')
    else:
        try:
            country = Country.objects.get(alias=country_alias)
        except Country.DoesNotExist:
            return HttpResponseRedirect('/countries/')

        if not country.show:
            return HttpResponseRedirect('/countries/')

        country_photos = country.get_photos()
        links = country.get_links()

        all_tours = country.get_all_tours()
        tours = all_tours.exclude(hot=True)
        hot_tours = all_tours.filter(hot=True)

        return render_to_response(
            'countries/country.html',
                {
                'country':country,
                'country_photos':country_photos,
                'links':links,
                'hot_tours':hot_tours,
                'tours':tours,
                'menu_url': u'/countries/'
            },
            context_instance=RequestContext(request, processors=[custom_proc])
        )

