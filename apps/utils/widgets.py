# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe


class Redactor(forms.Textarea):
    toolbar = u'classic' #'mini'
    class Media:
        js = (
            '/static/js/jquery.js',
            '/static/js/redactor/redactor.js',
            )
        css = {
            'all': ('/static/js/redactor/css/redactor.css',)
        }

    def __init__(self, attrs=None):
        self.attrs = attrs
        if attrs:
            self.attrs.update(attrs)
        super(Redactor,self).__init__(attrs)

    def render(self,name,value,attrs=None):
        rendered = super(Redactor,self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
        $(document).ready(
            function()
            {
                $('#id_%s').redactor({ focus: true,toolbar: '%s' });
            }
        );
        </script>''' % (name,self.toolbar))


class RedactorMini(Redactor):
    toolbar = u'mini'

class RedactorMicro(Redactor):
    toolbar = u'micro'

