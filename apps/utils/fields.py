# -*- coding: utf-8 -*-

from django.db import models
from django.utils import translation



class LanguageManager(models.Manager):
    def get_query_set(self):
        query = super(LanguageManager, self).get_query_set()
        if translation.get_language() == 'en':
            return query.filter(has_en_transl=True)
        return query



class TranslationModel(models.Model):
    has_en_transl = models.BooleanField(
        editable = False,
        verbose_name = u'eng',
        default = False,
    )

    # Managers
    objects = models.Manager()
    locale = LanguageManager()
