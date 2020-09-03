# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from setup_backend import create_inform_general
import backend.monitoring_report as report_generator

import os
from datetime import datetime

#--------- Domingo
# 1. Peticion de inicio de procesamiento to-do con darle al enlace
# 2. Preparar graficas, indicadores y pantalla de dashboard
# 3. Formulario de acceso vista
# 4. Gestion de centro y año

#---------- Lunes
# 1. Datos simulados de ocupación

#---------- Martes
# 1. Gestionar arquitectura de monitorizacion


def monitoring_menu(request):
    return render(request, "use_case/monitoring_menu.html")


def monitoring(request):
    #print("-------Init Server--------")
    #os.system('bash backend/streaming/control_spark.py &')
    #print("------------------------------")

    center = request.GET['center']
    con_person = request.GET['con_person']
    max_con = request.GET['max_con']

    informs_array_generate = ["""<script type="text/javascript"> 
            //setTimeout(function(){
            //   window.location.reload(1);
            //}, 7500);
        </script>
        """]

    informs_array_generate.append(report_generator.generate_header(int(center), 2013))

    # informs_array_generate.append("<h5 style='margin:0.5em 0 0 3em;'> Last update: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "</h5>")
    informs_array_generate.append("<h5 style='margin:0.5em 0 0 3em;'> Last update: 2018-01-01 21:13 </h5>")

    informs_array_generate.append(report_generator.generate_real_time(con_person=con_person, max_con=max_con))

    create_inform_general(informs_array=informs_array_generate, url="pems/templates/use_case/monitoring.html")
    return render(request, "use_case/monitoring.html", {})
