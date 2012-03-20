# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_protect

from django.conf import settings
from apps.pages.models import Page
from apps.utils.context_processors import custom_proc


def index(request):
    
    return direct_to_template(request, 'pages/index.html', locals())

DEFAULT_TEMPLATE = 'pages/page.html'

def page(request, url):

    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(Page, url__exact=url)
    if not f.is_published:
        raise Http404
    return render_page(request, f)


@csrf_protect
def render_page(request, f):
    t = loader.get_template(DEFAULT_TEMPLATE)

    menu_el_is_about = False
    if f.url == '/about/':
        menu_el_is_about =True

    c = RequestContext(request, {
        'page': f,
        'menu_el_is_about':menu_el_is_about
    },processors=[custom_proc])
    response = HttpResponse(t.render(c))

    return response