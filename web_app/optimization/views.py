# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from setup_backend import create_inform_general
import backend.monitoring_report as report_generator
import datetime


def optimization_menu(request):
    return render(request, "use_case/optimization_menu.html")


def optimization(request):
    return render(request, "use_case/optimization_menu.html")
