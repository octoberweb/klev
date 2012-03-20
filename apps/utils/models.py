# -*- coding: utf-8 -*-

from django.db import models

'''
from apps.utils.managers import LanguageManager



class TranslationModel(models.Model):
    has_en_transl = models.BooleanField(
        editable = False,
        verbose_name = u'eng',
        default = False,
    )
    # Managers
    objects = LanguageManager()

    class Meta:
        abstract = True

    @property
    def translated_to_en(self):
        raise NotImplementedError

    def save(self, **kwargs):
        self.has_en_transl = self.translated_to_en
        super(TranslationModel, self).save(**kwargs)
'''