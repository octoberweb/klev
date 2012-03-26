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
    cart_products = cart.get_products()
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

'''


@csrf_exempt
def get_photo_total(request):
    if request.is_ajax():
        if 'price' and 'val' in request.POST:
            price = int(request.POST['price'])
            try:
                val = int(request.POST['val'])
            except ValueError:
                return HttpResponse(u'symbol')

            sum = price * val

            return HttpResponse(u'%s %s' %(sum,choose_plural(sum, (u"рубль", u"рубля", u"рублей")) ))
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def get_cart_total_summary(request):
    if request.is_ajax():
        #sessionid = request.COOKIES['sessionid']
        sessionid = request.session.session_key

        if request.user.is_authenticated():
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(sessionid=sessionid)

        return HttpResponse(u'%s руб.' %cart.get_total_summary())
    else:
        return HttpResponseRedirect('/')





@csrf_exempt
def get_total_photo_from_cart(request):
    if request.is_ajax():
        if 'price' and 'count' in request.GET:
            try:
                price = int(request.GET['price'])
            except ValueError:
                return HttpResponseBadRequest()
            try:
                count = int(request.GET['count'])
            except ValueError:
                return HttpResponseBadRequest()

            sum = price * count

            return HttpResponse(u'%s %s' %(sum,choose_plural(sum, (u"рубль", u"рубля", u"рублей")) ))
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def update_cart_collage_personal(request):
    if request.is_ajax():
        if 'collage_personal_id' and 'option_id' in request.POST:
            try:
                collage_personal_id = int(request.POST['collage_personal_id'])
            except ValueError:
                return HttpResponseBadRequest()
            try:
                option_id = int(request.POST['option_id'])
            except ValueError:
                return HttpResponseBadRequest()

            try:
                collage_personal = CollagePersonal.objects.get(id=collage_personal_id)
            except CollagePersonal.DoesNotExist:
                return HttpResponseBadRequest()

            try:
                collage_option = CollageOption.objects.get(id=option_id)
            except CollageOption.DoesNotExist:
                return HttpResponseBadRequest()

            collage_personal.collage_option = collage_option
            collage_personal.save()


            return HttpResponse(u'collage_edited')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def delete_photo_from_cart(request):
    if request.is_ajax():
        if 'cart_photo_id' and 'stock_or_personal' in request.POST:
            try:
                cart_photo_id = int(request.POST['cart_photo_id'])
            except ValueError:
                return HttpResponseBadRequest()

            stock_or_personal = request.POST['stock_or_personal']

            if stock_or_personal == 'stock':
                try:
                    cart_photo = CartStockPhoto.objects.get(id=cart_photo_id)
                except CartStockPhoto.DoesNotExist:
                    return HttpResponseBadRequest()
            elif stock_or_personal == 'personal':
                try:
                    cart_photo = CartPersonalPhoto.objects.get(id=cart_photo_id)
                except CartPersonalPhoto.DoesNotExist:
                    return HttpResponseBadRequest()
            else:
                return HttpResponseBadRequest()

            cart_photo.delete()


            return HttpResponse(u'photo_deleted')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseRedirect('/')








@csrf_exempt
def update_cart(request):
    if request.is_ajax():
        if 'cart_photo_id' and 'count' and 'option_id' and 'stock_or_personal' in request.POST:

            try:
                cart_photo_id = int(request.POST['cart_photo_id'])
            except ValueError:
                return HttpResponseBadRequest()
            try:
                count = int(request.POST['count'])
            except ValueError:
                return HttpResponseBadRequest()

            option_id = request.POST['option_id']

            stock_or_personal = request.POST['stock_or_personal']
            if stock_or_personal == 'stock':
                try:
                    cart_photo = CartStockPhoto.objects.get(id=cart_photo_id)
                except CartStockPhoto.DoesNotExist:
                    return HttpResponseBadRequest()

                if option_id == u'el_form':
                    cart_photo.option = None
                    cart_photo.electronic_form = True

                else:
                    cart_photo.option = Option.objects.get(id=option_id)
                    cart_photo.electronic_form = False

                cart_photo.count = count
                cart_photo.save()
            elif stock_or_personal == 'personal':
                try:
                    cart_photo = CartPersonalPhoto.objects.get(id=cart_photo_id)
                except CartPersonalPhoto.DoesNotExist:
                    return HttpResponseBadRequest()

                if option_id == u'el_form':
                    cart_photo.option = None
                    cart_photo.electronic_form = True

                else:
                    cart_photo.option = Option.objects.get(id=option_id)
                    cart_photo.electronic_form = False

                cart_photo.count = count
                cart_photo.save()
            if option_id == u'el_form':
                cart_photo.option = None
                cart_photo.electronic_form = True

            else:
                cart_photo.option = Option.objects.get(id=option_id)
                cart_photo.electronic_form = False

            cart_photo.count = count
            cart_photo.save()
            return HttpResponse('cart_updated')
    else:
        return HttpResponseRedirect('/')






@csrf_exempt
def add_to_cart_personal_photo(request):
    if request.is_ajax():

        if 'option_id' in request.POST:
            option_id = request.POST['option_id']
            if option_id != 'el_form':
                try:
                    option_id = int(option_id)
                except ValueError:
                    return HttpResponseBadRequest()

                try:
                    option = Option.objects.get(id=option_id)
                except Option.DoesNotExist:
                    return HttpResponseBadRequest()

        else:
            return HttpResponseBadRequest()


        if 'quantity' in request.POST:
            quantity = request.POST['quantity']
            try:
                quantity = int(quantity)
            except ValueError:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


        if 'photo_id' in request.POST:
            photo_id = request.POST['photo_id']
            try:
                photo_id = int(photo_id)
            except ValueError:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()

        try:
            personal_photo = PersonalPhoto.objects.get(id=photo_id)
        except PersonalPhoto.DoesNotExist:
            return HttpResponseBadRequest()


        #sessionid = request.COOKIES['sessionid']
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


        if option_id == 'el_form':
            try:
                cart_personal_photo = CartPersonalPhoto.objects.get(
                    cart=cart,
                    personal_photo=personal_photo,
                    electronic_form=True
                )
                cart_personal_photo.count += quantity
                cart_personal_photo.save()
            except CartPersonalPhoto.DoesNotExist:
                cart_personal_photo = CartPersonalPhoto.objects.create(
                    cart=cart,
                    personal_photo=personal_photo,
                    count=quantity,
                    electronic_form=True
                )

        else:
            try:
                cart_personal_photo = CartPersonalPhoto.objects.get(
                    cart=cart,
                    personal_photo=personal_photo,
                    electronic_form=False,
                    option=option
                )
                cart_personal_photo.count += quantity
                cart_personal_photo.save()
            except CartPersonalPhoto.DoesNotExist:
                cart_personal_photo = CartPersonalPhoto.objects.create(
                    cart=cart,
                    personal_photo=personal_photo,
                    count=quantity,
                    electronic_form=False,
                    option=option
                )

        cart_html = render_to_string(
            'cart_inclusion.html',
            {'cart':cart}
        )

        return HttpResponse(cart_html)
    else:
        return HttpResponseRedirect('/')




@csrf_exempt
def add_to_cart_collage_personal(request):
    if request.is_ajax():
        if 'option_id' and 'photo_id_list' in request.POST:
            try:
                option_id = int(request.POST['option_id'])
            except ValueError:
                return HttpResponseBadRequest()

            photo_id_list = request.POST['photo_id_list'].split(',')

            personal_photos = PersonalPhoto.objects.filter(id__in=photo_id_list)

            try:
                option = CollageOption.objects.get(id=option_id)
            except CollageOption.DoesNotExist:
                return HttpResponseBadRequest()

            collage_personal = CollagePersonal.objects.create(
                collage_option = option
            )
            for personal_photo in personal_photos:
                collage_personal.personal_photo.add(personal_photo)


            #sessionid = request.COOKIES['sessionid']
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

            cart.collage_personal.add(collage_personal)

            return HttpResponse('collage_created')


        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def edit_cart_collage_personal(request):
    if request.is_ajax():
        if 'option_id' and 'photo_id_list' and 'collage_id' in request.POST:
            try:
                option_id = int(request.POST['option_id'])
            except ValueError:
                return HttpResponseBadRequest()

            try:
                collage_id = int(request.POST['collage_id'])
            except ValueError:
                return HttpResponseBadRequest()


            try:
                collage_personal = CollagePersonal.objects.get(id=collage_id)
            except CollagePersonal:
                return HttpResponseBadRequest()

            #sessionid = request.COOKIES['sessionid']
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

            if collage_personal not in cart.get_collage_personal():
                return HttpResponseBadRequest()


            photo_id_list = request.POST['photo_id_list'].split(',')
            personal_photos = PersonalPhoto.objects.filter(id__in=photo_id_list)

            try:
                option = CollageOption.objects.get(id=option_id)
            except CollageOption.DoesNotExist:
                return HttpResponseBadRequest()

            collage_personal.collage_option = option
            collage_personal.save()

            collage_personal.personal_photo.clear()
            for personal_photo in personal_photos:
                collage_personal.personal_photo.add(personal_photo)




            cart.collage_personal.add(collage_personal)

            return HttpResponse('collage_edited')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseRedirect('/')





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

    options = Option.objects.order_by('-order')
    collage_options = CollageOption.objects.order_by('-order')

    return render_to_response(
        'cart.html',
        {
            'cart':cart,
            'options':options,
            'collage_options':collage_options
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )





@csrf_exempt
def confirm_order(request):
    if request.is_ajax():
        if 'profile_name' and 'profile_telephone' in request.POST:
            #sessionid = request.COOKIES['sessionid']
            sessionid = request.session.session_key

            user = request.user
            if user.is_authenticated():
                try:
                    cart = Cart.objects.get(user=user)
                except Cart.DoesNotExist:
                    cart = False
            else:
                try:
                    cart = Cart.objects.get(sessionid=sessionid)
                except Cart.DoesNotExist:
                    cart = False

            if cart:
                if user.is_authenticated():
                    order = Order.objects.create(
                        user=user,
                        name=request.POST['profile_name'],
                        telephone=request.POST['profile_telephone'],
                        comment=request.POST['order_comment']
                    )
                else:
                    order = Order.objects.create(
                        name=request.POST['profile_name'],
                        telephone=request.POST['profile_telephone'],
                        comment=request.POST['order_comment']
                    )

                cart_get_personal_photos = cart.get_personal_photos()
                if cart_get_personal_photos:
                    for cart_personal_photo in cart_get_personal_photos:
                        if cart_personal_photo.electronic_form:
                            OrderPersonalPhoto.objects.create(
                                order=order,
                                count=cart_personal_photo.count,
                                personal_photo=cart_personal_photo.personal_photo,
                                electronic_form=True
                            )
                        else:
                            OrderPersonalPhoto.objects.create(
                                order=order,
                                count=cart_personal_photo.count,
                                personal_photo=cart_personal_photo.personal_photo,
                                option=cart_personal_photo.option

                            )

                cart_get_stock_photos = cart.get_stock_photos()
                if cart_get_stock_photos:
                    for cart_stock_photo in cart_get_stock_photos:
                        if cart_stock_photo.electronic_form:
                            OrderStockPhoto.objects.create(
                                order=order,
                                count=cart_stock_photo.count,
                                stock_photo=cart_stock_photo.stock_photo,
                                electronic_form=True
                            )
                        else:
                            OrderStockPhoto.objects.create(
                                order=order,
                                count=cart_stock_photo.count,
                                stock_photo=cart_stock_photo.stock_photo,
                                option=cart_stock_photo.option

                            )
                cart_get_collage_personal = cart.get_collage_personal()
                if cart_get_collage_personal:
                    for cart_collage_personal in cart_get_collage_personal:
                        order.collage_personal.add(cart_collage_personal)

                cart.delete()

                if settings.SERVER_SETTINGS and user.email:
                    current_site = Site.objects.get_current()

                    subject = u'Vidmax - Ваша заказ'

                    subject = u''.join(subject.splitlines())

                    message = render_to_string(
                        'order_print_version.html',
                        {'order':order}
                    )

                    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                    msg.content_subtype = "html"
                    msg.send()


                return HttpResponse('order_confirmed')


            else:
                return HttpResponseBadRequest()

            #return HttpResponse(u'collage_edited')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseRedirect('/')



def order_confirmed(request):
    return render_to_response(
        'order_confirmed.html',
        context_instance=RequestContext(request, processors=[custom_proc])
    )



def print_version_of_order(request, order_id):
    try:
        order_id = int(order_id)
    except ValueError:
        raise Http404


    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise Http404

    return render_to_response(
        'order_print_version.html',
        {
            'order':order
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )


def get_order_rules(request):
    try:
        rules = Text.objects.get(unique_name=u'order_rules')
    except Text.DoesNotExist:
        return HttpResponseBadRequest()


    return HttpResponse(rules.text)


'''