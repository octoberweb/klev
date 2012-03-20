# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from faq.forms import QuestionForm, ReportForm
from faq.models import Question, Report, QuestionCategory
from context_processors import custom_proc



def questions_list(request, page=1, category_alias=None):
    page = int(page)


    questions = Question.objects.filter(published = True)

    if category_alias is not None:
        try:
            category = QuestionCategory.objects.get(alias=category_alias)
        except QuestionCategory:
            raise Http404

        questions = questions.filter(category=category)

    questions = questions.order_by("-pub_date")
    paginator = Paginator(questions,15)

    try:
        questions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        questions = paginator.page(paginator.num_pages)

    plus2 = False
    plus3 = False
    if questions.has_next():
        page1 = page + 1
        plus2 = paginator.page(page1)

        if plus2:
            if plus2.has_next():
                page2 = page + 2
                plus3 = paginator.page(page2)


    form = QuestionForm()

    categories = QuestionCategory.objects.all()
    categories = categories.order_by('-order')

    return render_to_response(
            'faq.html',
            {'questions':questions,
             'plus2':plus2,
             'plus3':plus3,
             'form':form,
             'category_alias':category_alias,
             'categories':categories
            },
            context_instance=RequestContext(request, processors=[custom_proc])
        )



def reports_list(request, page=1):
    try:
        page = int(page)
    except ValueError:
        page = 1

    reports = Report.objects.filter(published = True)
    reports = reports.order_by("-pub_date")
    paginator = Paginator(reports,15)

    try:
        reports = paginator.page(page)
    except (EmptyPage, InvalidPage):
        reports = paginator.page(paginator.num_pages)

    plus2 = False
    plus3 = False
    if reports.has_next():
        page1 = page + 1
        plus2 = paginator.page(page1)

        if plus2:
            if plus2.has_next():
                page2 = page + 2
                plus3 = paginator.page(page2)

    form = ReportForm()

    return render_to_response(
            'feedbacks.html',
            {'reports':reports,
             'plus2':plus2,
             'plus3':plus3,
             'form':form
            },
            context_instance=RequestContext(request, processors=[custom_proc])
        )

@csrf_exempt
def send_question(request):
    if request.is_ajax:
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
            faq_form_html = render_to_string(
                    'faq_form.html',
                    {'form':form}
                )

            return HttpResponse(faq_form_html)


    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def send_report(request):
    if request.is_ajax:
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
            feedback_form_html = render_to_string(
                    'feedback_form.html',
                    {'form':form}
                )

            return HttpResponse(feedback_form_html)

    else:
        return HttpResponseRedirect('/')



