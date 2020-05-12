# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader

import setup_backend as backend

import backend.general_report as report_generator
from setup_backend import create_inform_general

"""
    Script que esta preparado para gestionar los metodos de solar. Cargar los html.
"""

def solar_menu(request):
    return render(request, "use_case/solar_menu.html")

def solar_report(request):

    date = request.GET['date']
    center = request.GET['center']
    kpi = request.GET['kpi']
    consume = request.GET['consume']

    # Header section
    informs_array_generate = [report_generator.generate_header(center = center, date = date)]
    
    # Table and general sensor graphic 
    informs_array_generate.append(str(report_generator.generate_general_sensor_data(center = center, date = date)))

    # TODO
    # KPI sensor
    if kpi == "3" or kpi == "2": 
        informs_array_generate.append(str(report_generator.sensor_kpi_general(center = center, date = date)))

    # Table and general solar graphic 
    informs_array_generate.append(str(report_generator.generate_general_solar_data(center = center, date = date)))
    
    # KPI solar
    if kpi == "4" or kpi == "2": 
        informs_array_generate.append(str(report_generator.solar_kpi_general(center = center, date = date)))
    
    # Consume

    create_inform_general(informs_array = informs_array_generate)

    return render(request, "use_case/solar.html", {})