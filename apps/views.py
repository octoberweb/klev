# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import loader, RequestContext, Context
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from apps.utils.context_processors import custom_proc


def index(request):

    return render_to_response(
        'index.html',
        {
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )