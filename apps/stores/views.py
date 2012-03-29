# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import loader, RequestContext, Context
from django.http import *

from apps.utils.context_processors import custom_proc
from apps.stores.models import Store



def view_stores(request):
    stores = Store.items.all()

    return render_to_response(
        'stores/stores.html',
        {
            'stores':stores,
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )



