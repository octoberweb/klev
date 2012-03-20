# -*- coding: utf-8 -*-
from django.contrib import admin
from faq.models import Question, Report, QuestionCategory


class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'alias', 'order','show_on_footer')
    list_display_links = ('id','name', 'alias', )

admin.site.register(QuestionCategory, QuestionCategoryAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','pub_date','category', 'published',)
    list_display_links = ('id','pub_date','category', )
    search_fields = ('question', 'answer',)
    list_filter = ('pub_date','category', 'published',)

admin.site.register(Question, QuestionAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id','pub_date','name', 'published',)
    list_display_links = ('id','pub_date', 'name',)
    search_fields = ('report',)
    list_filter = ('pub_date','published',)

admin.site.register(Report, ReportAdmin)