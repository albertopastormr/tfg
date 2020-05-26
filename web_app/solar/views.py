# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import backend.general_report as report_generator
import backend.specific_report as specific_generator

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

    panels = request.GET['panels']
    consume_batteries = request.GET['consume_batteries']

    control_batteries = request.GET['batteries_control']
    n_serie_batteries = request.GET['n_serie_batteries']
    batteries_power = request.GET['batteries_power']
    minimal_dicharging_percent = request.GET['minimal_dicharging_percent']

    active_vs_reactive = request.GET['active_reactive']

    # Header section
    informs_array_generate = [report_generator.generate_header(center=center, date=date)]

    # Table and general sensor graphic 
    informs_array_generate.append(str(report_generator.generate_general_sensor_data(center=center, date=date)))

    # TODO
    # KPI sensor
    if kpi == "3" or kpi == "2":
        informs_array_generate.append("<h1> Kpis Sensor </h1>")
        informs_array_generate.append(str(report_generator.sensor_kpi_general(center=center, date=date)))

    # Table and general solar graphic
    informs_array_generate.append(str(report_generator.generate_general_solar_data(center=center, date=date)))

    # KPI solar
    if kpi == "4" or kpi == "2":
        informs_array_generate.append("<h1> Kpis Solar </h1>")
        informs_array_generate.append(str(report_generator.solar_kpi_general(center=center, date=date)))

    # Active vs Reactive
    if active_vs_reactive == "2":
        informs_array_generate.append("<h1> Active vs Reactive </h1>")
        informs_array_generate.append(str(report_generator.sensor_active_vs_reactive(center=center, date=date)))

    # Consume Hourly
    if consume == "3" or consume == "2":
        informs_array_generate.append("<h1> Consume Hourly </h1>")
        informs_array_generate.append(
            str(specific_generator.consume_hourly_generic(center=center, date=date, num_panels=int(panels))))

    # Consume Monthly
    if consume == "4" or consume == "2":
        informs_array_generate.append("<h1> Consume Month </h1>")
        informs_array_generate.append(
            str(specific_generator.generate_analysis_month(center=center, date=date, num_panels=int(panels))))

    # Consume with Batteries
    if control_batteries == "2":
        informs_array_generate.append("<h1> Batteries </h1>")
        informs_array_generate.append(
            str(specific_generator.consume_hourly_with_batteries(center=center, date=date,
                                                                 num_panels=int(consume_batteries),
                                                                 number_serie_batteries=int(n_serie_batteries),
                                                                 power_battery=int(batteries_power),
                                                                 min_discharging_percent=int(minimal_dicharging_percent)
                                                                 )
                )
        )

    create_inform_general(informs_array=informs_array_generate)

    return render(request, "use_case/solar.html", {})
