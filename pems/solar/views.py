# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader

"""
    Script que esta preparado para gestionar los metodos de solar. Cargar los html.
"""

def solar_menu(request):
    return render(request, "use_case/solar_menu.html")

def solar_report(request):

    if request.GET['id_type'] == "1":

        return render(request, "use_case/solar.html", {"center":request.GET['id_center']})
    else:
        return HttpResponse("Request que no es general: %r" % request.GET['id_type'])


    