# -*- coding: utf-8 -*-
from apps.utils.forms import RegForm, AuthForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site

def random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    from random import choice
    return ''.join([choice(allowed_chars) for i in range(length)])

def receipt_of_orders(request, OrderForm):
    send = False
    registration = False
    auth = False
    order = False
    form_order = OrderForm(data=request.POST)
    if request.POST.has_key('_order'):
        if form_order.is_valid():
            if request.user.is_authenticated():
                form_order.instance.user = request.user
                form_order.save()
                send = True
                return False, form_order, False, auth, order, registration, send
            else:
                order = True
                registration = True
                form_registration = RegForm()
                form_auth = AuthForm()
                return form_auth, form_order, form_registration, auth, order, registration, send
        else:
            return False, form_order, False, auth, order, registration, send
    else:
        if request.POST.has_key('_auth'):
            form_auth = AuthForm(data=request.POST)
            form_registration = RegForm()
            order = True
            auth = True
            if form_auth.is_valid():
                auth_login(request, form_auth.get_user())
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                form_order.instance.user = request.user
                form_order.save()
                send = True
                return form_auth, form_order, form_registration, auth, order, registration, send
            else:
                return form_auth, form_order, form_registration, auth, order, registration, send
        else:
            if request.POST.has_key('_registration'):
                new_pass = random_password(length=5)
                my_data = request.POST.copy()
                my_data['username'] = my_data['email']
                my_data['password1'] = new_pass
                my_data['password2'] = new_pass
                form_registration = RegForm(my_data)
                form_auth = AuthForm()
                order = True
                registration = True
                if form_registration.is_valid():
                    new_user = form_registration.save()
                    user = User.objects.get(username = my_data['username'])
                    user.first_name = my_data['name']
                    user.save()
                    profile = user.get_profile()
                    profile.phone = my_data['phone']
                    profile.save()
                    form_order.instance.user = new_user
                    form_order.save()
                    send = True
                    return form_auth, form_order, form_registration, auth, order, registration, send
                else:
                    return form_auth, form_order, form_registration, auth, order, registration, send
    return False, form_order, False, auth, order, registration, send

def send_order_email(subject, html_content):

    email_list =[u'alekssei1@yandex.ru',]
    current_site = Site.objects.get_current()

    email_from = u'«Панама - Мир Развлечений» <reply@%s>' % current_site.domain
    text_content = u''

    if email_list:
        msg = EmailMultiAlternatives(subject, text_content, email_from, email_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()