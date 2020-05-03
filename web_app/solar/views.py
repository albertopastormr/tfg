# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader

import setup_backend as backend

"""
    Script que esta preparado para gestionar los metodos de solar. Cargar los html.
"""

def solar_menu(request):
    return render(request, "use_case/solar_menu.html")

def solar_report(request):

    date = request.GET['date']
    center = request.GET['id_center']

    if request.GET['id_type'] == "1":

        # Insertar argumentos de fecha y centro a pedir
        backend.create_inform_general(center = center, date = date)

        return render(request, "use_case/solar.html", {"center":request.GET['id_center']})
    else:
        return HttpResponse("Request que no es general: %r" % request.GET['id_type'])


    