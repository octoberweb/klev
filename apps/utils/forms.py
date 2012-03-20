# -*- coding: utf-8 -*-
from django import forms
from apps.users.forms import RegistrationFormUniqueEmail
from django.contrib.auth.forms import AuthenticationForm

class RegForm(RegistrationFormUniqueEmail):

    username = forms.CharField(max_length=50)
    name = forms.CharField(label=u'Имя', max_length=100, widget=forms.TextInput(attrs = {"placeholder": "Имя"}))
    email = forms.EmailField(widget=forms.TextInput(attrs = {"placeholder": "E-mail"}))
    phone = forms.CharField(label=u'Телефон', max_length=50, widget=forms.TextInput(attrs = {"placeholder": "Номер телефона"}))

class AuthForm(AuthenticationForm):

    username = forms.EmailField(widget=forms.TextInput(attrs = {"placeholder": "E-mail"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs = {"placeholder": "Пароль"}))

