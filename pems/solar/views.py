# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

"""
    Script que esta preparado para gestionar los metodos de solar. Cargar los html.
"""

def solar(request):
    template = loader.get_template('use_case/solar_menu.html')
    context = {}
    return HttpResponse(template.render(context, request))