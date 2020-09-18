# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from setup_backend import create_inform_general
import backend.monitoring_report as report_generator
import datetime
import backend.optimization


def optimization_menu(request):
    return render(request, "use_case/optimization_menu.html")

def optimization_test(request):

    center = request.GET['center']
    budget = request.GET['budget']
    con_demanded = request.GET['con_demanded']
    
    return render(request, "use_case/optimization.html", {})
