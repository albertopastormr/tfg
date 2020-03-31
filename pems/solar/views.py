# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

def solar(request):
    template = loader.get_template('solar/prueba_1.html')
    context = {}
    return HttpResponse(template.render(context, request))