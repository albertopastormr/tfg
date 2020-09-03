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
    informs_array_generate = [report_generator.generate_header(center=center, date=2018)]

    # Table and general sensor graphic
    informs_array_generate.append("<div style='width:80%; margin: auto;'><h3 style='text-align: center;'> Datos de consumo del centro </h3> </br></br>")
    informs_array_generate.append("<div style='width:100%; margin: auto;'> A continuación se muestran los datos de consumo generales para el centro específicado. "
                                  "Se contiene la tabla con todos los datos para el año específico y una gráfica temporal donde "
                                  "por defecto aparece el último mes y puedes con los botones o la propia interación de la gráfica "
                                  "dictar un espacio temporal diferentes.</div></div>")
    informs_array_generate.append(str(report_generator.generate_general_sensor_data(center=center, date=date)))

    # KPI sensor
    if kpi == "3" or kpi == "2":
        informs_array_generate.append(
            "<div style='width:80%; margin: auto;'><h3 style='text-align: center;'> Estudio analítico de consumo del "
            "centro dando información general de los datos para un centro especificado.</h3></br></br>")
        informs_array_generate.append(
            "<div style='width:100%; margin: auto;'> Un análisis general de la energia del centro que muestran resultados "
            "de calculos estadisticos para su conocimiento.</div></div>")
        informs_array_generate.append(str(report_generator.sensor_kpi_general(center=center, date=date)))

    # Table and general solar graphic
    informs_array_generate.append(
        "</br></br><div style='width:80%; margin: auto;'><h3 style='text-align: center;'> Datos de energía fotovoltaica </h3> </br></br>")
    informs_array_generate.append(
        "<div style='width:100%; margin: auto;'> A continuación se muestran los datos de energía fotovoltaica del centro escogido. "
        "La información se trata con 2 paneles solares por horas y angulos más óptimos."
        "Se contiene la tabla con todos los datos para el año específico y una gráfica temporal donde "
        "por defecto aparece el último mes y puedes con los botones o la propia interación de la gráfica "
        "dictar un espacio temporal diferentes.</div></div>")
    informs_array_generate.append(str(report_generator.generate_general_solar_data(center=center, date=date)))

    # KPI solar
    if kpi == "4" or kpi == "2":
        informs_array_generate.append(
            "<div style='width:80%; margin: auto;'><h3 style='text-align: center;'> Detalles sobre energia solar </h3> </br></br>")
        informs_array_generate.append(
            "<div style='width:100%; margin: auto;'> Diferentes datos específicos de la energia fotovoltaica que muestran información "
            "de la tecnologia de la placa solar usada, así como configuración usada.</div></div>")
        informs_array_generate.append(str(report_generator.solar_kpi_general(center=center, date=date)))

    # Active vs Reactive
    if active_vs_reactive == "2":
        informs_array_generate.append(
            "<div style='width:80%; margin: auto;'><h3 style='text-align: center;'> Active vs Reactive Energy </h3> </br></br>")
        informs_array_generate.append(
            "<div style='width:100%; margin: auto;'> La siguiente gráfica temporal muestra la comparativa entre energias reactiva y activa."
            " También se muestra la información de la energia máxima dictada por el centro.</div></div>")
        informs_array_generate.append(str(report_generator.sensor_active_vs_reactive(center=center, date=date)))

    # Consume Hourly
    if consume == "3" or consume == "2":
        informs_array_generate.append(
            "<div style='width:80%; margin: auto;'><h3 style='text-align: center;'> Consumo por horas </h3> </br></br>")
        informs_array_generate.append(
            "<div style='width:100%; margin: auto;'> Gráficas que muestran una estimación del consumo por horas del centro con el "
            "uso de {} paneles solares con la configuración óptima. Se muestran dos gráficas, una con el consumo en kw/h "
            "y otra con el coste estimado en €.</div></div>".format(panels))
        informs_array_generate.append(
            str(specific_generator.consume_hourly_generic(center=center, date=date, num_panels=int(panels))))

    # Consume Monthly
    if consume == "4" or consume == "2":
        informs_array_generate.append(
            "<div style='width:80%; margin: auto;'><h3 style='text-align: center;'> Consumo mensual </h3> </br></br>")
        informs_array_generate.append(
            "<div style='width:100%; margin: auto;'> Gráficas que muestran una estimación del consumo por meses del centro. "
            "Se muestran dos gráficas, una sin placas solares y la otra con {} paneles solares con la configuración óptima."
            "Las dos gráficas tienen dos columnas de datos, una con el consumo en kw/h y otra en €.</div></div>".format(panels))
        informs_array_generate.append(
            str(specific_generator.generate_analysis_month(center=center, date=date, num_panels=int(panels))))

    # Consume with Batteries
    if control_batteries == "2":
        informs_array_generate.append(
            "<div style='width:80%; margin: auto;'><h3 style='text-align: center;'> Energía con baterias </h3> </br></br>")
        informs_array_generate.append(
            "<div style='width:100%; margin: auto;'> La gráfica que se muestra a continuación muestra el consumo en kw/h"
            " por horas en el año y centro seleccionados con el uso de baterias y placasa solares, las especificaciones de estos"
            " dos componentes han sido ingresadas en el formulario correspondiente.</div></div>".format(panels))
        informs_array_generate.append(
            str(specific_generator.consume_hourly_with_batteries(center=center, date=date,
                                                                 num_panels=int(consume_batteries),
                                                                 number_serie_batteries=int(n_serie_batteries),
                                                                 power_battery=int(batteries_power),
                                                                 min_discharging_percent=int(minimal_dicharging_percent)
                                                                 )
                )
        )

    informs_array_generate.append("</br></br>")

    create_inform_general(informs_array=informs_array_generate, url="pems/templates/use_case/solar.html")
    return render(request, "use_case/solar.html", {})
