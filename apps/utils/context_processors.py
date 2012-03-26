# -*- coding: utf-8 -*-
from apps.meta.models import Meta
from django.contrib.auth.forms import AuthenticationForm

from apps.products.models import Section
from apps.stores.models import Store

def custom_proc(request):
    try:
        meta = Meta.objects.get(url = request.path)
    except Meta.DoesNotExist:
        meta = False

    user = request.user
    current_url = request.path

    sections = Section.items.all()
    stores = Store.items.all()

    return {
        'meta': meta,
        'user': user,
        'current_url':current_url,
        'sections':sections,
        'stores':stores,
        'sessionid': request.session.session_key,

    }