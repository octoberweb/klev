# -*- coding: utf-8 -*-
from django import forms
from faq.models import Question, Report

class QuestionForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'active_input'}), required=True)

    class Meta:
        model = Question
        fields = ('email', 'question',)


class ReportForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'active_input'}), required=True)
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'active_input'}), required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'active_input'}), required=False)

    class Meta:
        model = Report
        fields = ('name','city','email','report',)