# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _

class QuestionCategory(models.Model):
    name = models.CharField(max_length = 150, verbose_name = u'Название')
    alias = models.CharField(verbose_name=u'Алиас', max_length=100, help_text=u'Уникальное имя на латинице, без пробелов',unique=True)
    order = models.IntegerField(verbose_name=u'Порядок сортировки', help_text=u'Чем больше число, тем выше элемент', default=10)

    class Meta:
        verbose_name = _(u'category')
        verbose_name_plural = _(u'categories')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u'/faq/%s/' %self.alias

class Question(models.Model):
    category = models.ForeignKey(QuestionCategory, verbose_name=u'Категория', blank=True, null=True)
    pub_date = models.DateTimeField(verbose_name = u'Дата', default=datetime.datetime.now)
    name = models.CharField(max_length = 150, verbose_name = u'Имя')
    email = models.CharField(verbose_name=u'E-mail',max_length=75)
    question = models.TextField(verbose_name = u'Вопрос')
    answer = models.TextField(verbose_name = u'Ответ', blank = True)
    published = models.BooleanField(verbose_name = u'Опубликовано', default=False)

    class Meta:
        verbose_name = _(u'question')
        verbose_name_plural = _(u'questions')

    def __unicode__(self):
        return u'Вопрос от %s' % self.pub_date

    def get_absolute_url(self):
        return u'/faq/#question_%i' %self.id

