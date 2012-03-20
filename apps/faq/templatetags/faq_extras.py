# -*- coding: utf-8 -*-
from faq.models import *
from django import template

register = template.Library()



@register.inclusion_tag("question_last.html")
def get_question_last():
    questions = Question.objects.filter(published=True)
    questions = questions.order_by('-pub_date')
    if questions.count() >3:
        return {'questions': questions[:3]}
    else:
        return {'questions': questions}


@register.inclusion_tag("footer_menu_from_faq.html")
def get_footer_menu_from_faq():
    categories = QuestionCategory.objects.filter(show_on_footer=True)
    return {'categories': categories}
