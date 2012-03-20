# -*- coding: utf-8 -*-
from apps.meta.models import Meta
from django.contrib.auth.forms import AuthenticationForm

def custom_proc(request):
    try:
        meta = Meta.objects.get(url = request.path)
    except Meta.DoesNotExist:
        meta = False

    user = request.user
    current_url = request.path

    return {
        'meta': meta,
        'user': user,
        'current_url':current_url,

    }