# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from string import split

register = template.Library()
from apps.products.models import Param, Product


@register.inclusion_tag("products/item.html")
def get_product_html(product, product_category='True'):
    if product_category == 'False':
        product_category= False

    return {
        'product': product,
        'product_category':product_category,
    }

@register.inclusion_tag('products/catalog_params.html',takes_context=True)
def getvars(context, objects, param, props='not_props' ):
    if  props == 'not_props':
        props = False
    elif props == 'props':
        props = True

    to_return = {
        'objects':objects,
        'param':param,
        'props':props
    }
    if 'request' in context:
        getvars = context['request'].GET.copy()
        if param in getvars:
            param_value = getvars[param]
            if param=='subcategory' or param=='storage':
                try:
                    param_value = int(param_value)
                except ValueError:
                    param_value = False
            to_return['param_value'] = param_value
            del getvars[param]

        keys = getvars.keys()
        len_getvars_keys = len(keys)

        if len_getvars_keys > 0:
            to_return['getvars'] = "&%s" % getvars.urlencode()
            if param=='subcategory':
                for key in keys:
                    if key!='storage':
                        del getvars[key]
            to_return['getvars_all'] = "%s" % getvars.urlencode()

        else:
            to_return['getvars'] = ''

    return to_return

@register.inclusion_tag('products/catalog_params_props.html',takes_context=True)
def getvars_properties(context, property, products, property_alias):
    objects = Param.objects.distinct().select_related().filter(product__in=list(products)).filter(property=property).values('value')
    return {
        'objects':objects,
        'property_alias':property_alias,
        'request':context['request']
    }
