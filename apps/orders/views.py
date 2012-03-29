# -*- coding: utf-8 -*-
from django.contrib import auth
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import  render_to_response

from django.forms.models import inlineformset_factory
from django.template import loader, RequestContext, Context

from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.mail import EmailMessage
from pytils.numeral import choose_plural
from django.views.decorators.csrf import csrf_exempt

from apps.utils.context_processors import custom_proc
from apps.products.models import Product
from apps.orders.models import Cart, CartProduct



def view_cart(request):
    #sessionid = request.COOKIES['sessionid']
    sessionid = request.session.session_key

    if request.user.is_authenticated():
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = False
    else:
        try:
            cart = Cart.objects.get(sessionid=sessionid)
        except Cart.DoesNotExist:
            cart = False

    is_empty = True
    if cart:
        cart_products = cart.get_products()
    else:
        cart_products = False

    cart_str_total = u''
    if cart_products:
        is_empty = False
        cart_str_total = cart.get_str_total()
    return render_to_response(
        'orders/cart.html',
        {
            'is_empty':is_empty,
            'cart_products':cart_products,
            'cart_str_total':cart_str_total
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )


@csrf_exempt
def add_product_to_cart(request):
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    else:
        if 'product_id' not in request.POST:
            return HttpResponseBadRequest()
        else:

            product_id = request.POST['product_id']
            try:
                product_id = int(product_id)
            except ValueError:
                return HttpResponseBadRequest()

        try:
            product = Product.items.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponseBadRequest()


        sessionid = request.session.session_key

        if request.user.is_authenticated():
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=request.user,sessionid=sessionid)
        else:
            try:
                cart = Cart.objects.get(sessionid=sessionid)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(sessionid=sessionid)



        try:
            cart_product = CartProduct.objects.get(
                cart=cart,
                product=product
            )
            cart_product.count += 1
            cart_product.save()
        except CartProduct.DoesNotExist:
            CartProduct.objects.create(
                cart=cart,
                product=product
            )
        is_empty = True
        cart_products_count = cart.get_products_count()
        cart_total = cart.get_str_total()
        cart_products_text = u''
        if cart_products_count:
            is_empty = False
            cart_products_text = u'товар%s' %(choose_plural(cart_products_count,(u'',u'а',u'ов')))

        cart_html = render_to_string(
            'orders/cart_block.html',
            {
                'is_empty':is_empty,
                'cart_products_count':cart_products_count,
                'cart_total':cart_total,
                'cart_products_text':cart_products_text
            }
        )

        return HttpResponse(cart_html)

@csrf_exempt
def delete_product_from_cart(request):
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    else:
        if 'cart_product_id' not in request.POST:
            return HttpResponseBadRequest()
        else:

            cart_product_id = request.POST['cart_product_id']
            try:
                cart_product_id = int(cart_product_id)
            except ValueError:
                return HttpResponseBadRequest()

        try:
            cart_product = CartProduct.objects.get(id=cart_product_id)
        except CartProduct.DoesNotExist:
            return HttpResponseBadRequest()

        cart_product.delete()


        sessionid = request.session.session_key

        if request.user.is_authenticated():
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=request.user,sessionid=sessionid)
        else:
            try:
                cart = Cart.objects.get(sessionid=sessionid)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(sessionid=sessionid)


        is_empty = True
        cart_products_count = cart.get_products_count()
        cart_total = u''
        cart_products_text = u''
        if cart_products_count:
            cart_total = cart.get_str_total()
            is_empty = False
            cart_products_text = u'товар%s' %(choose_plural(cart_products_count,(u'',u'а',u'ов')))

        cart_html = render_to_string(
            'orders/cart_block.html',
            {
                'is_empty':is_empty,
                'cart_products_count':cart_products_count,
                'cart_total':cart_total,
                'cart_products_text':cart_products_text
            }
        )
        cart_html = cart_html.replace(u'    ',u'').replace(u'\n',u'')
        data = u'''{"cart_html":'%s',"cart_total":'%s'}'''%(cart_html,cart_total)

        return HttpResponse(data)
