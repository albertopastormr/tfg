#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pprint
import xmltodict
from datetime import *
from dateutil.relativedelta import *
import plotly.graph_objects as go
import pandas as pd
import xml.etree.ElementTree as et
import plotly.graph_objs as go
import plotly.express as px
import plotly
import plotly.io as pio
from django.utils.encoding import smart_str
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from dateutil import parser
import math
from calendar import monthrange


def get_methods(object, spacing=20):
    methodList = []
    for method_name in dir(object):
        try:
            if callable(getattr(object, method_name)):
                methodList.append(str(method_name))
        except:
            methodList.append(str(method_name))
    processFunc = (lambda s: ' '.join(s.split())) or (lambda s: s)
    for method in methodList:
        try:
            print(str(method.ljust(spacing)) + ' ' +
                  processFunc(str(getattr(object, method).__doc__)[0:90]))
        except:
            print(method.ljust(spacing) + ' ' + ' getattr() failed')

        # De https://plot.ly/python/v3/html-reports/


def generarHTML(fig):
    html_string = '''
 <html>
     <head>
     
<meta charset="UTF-8">

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
  <link rel="stylesheet" href="estilo.css">
  <style>body{ margin:0 100; background:whitesmoke; }</style>
     </head>
     <body>

  <h2>Estado de la UCM</h2>
  ''' + fig + '''
 <h2>Zonas donde se detectan variaciones</h2>
     </body>
 </html>'''
    return html_string


def generaResumenCentroVariableMedia(centro, datosTotales, datosAnyoAnterior, datosAnyoActual, variable):
    datos = datosAnyoActual[datosAnyoActual["centro"] == centro]
    datos18 = datosAnyoAnterior[datosAnyoAnterior["centro"] == centro]
    consumoActual = 0.0
    consumoPasado = 0.0
    contador = 0
    for i, row in datos18.iterrows():
        time = row["fecha"]  # datetime.strptime(row["fecha"], timeformat)
        time = time.replace(year=time.year + 1)
        #datos18.set_value(i, "fecha", time)
        # Se quiere contabilizar sólo aquellos meses para los que se tenga factura en el año en curso
        if (len(datos[datos.fecha == time].index) == 1):  # time.strftime(timeformat)]) == 1):
            # print(datos[datos.fecha == time.strftime("%Y-%m-%d")])
            # print(int(datos[datos.fecha == time.strftime("%Y-%m-%d")]["consumo"]))
            consumoActual = consumoActual + int(datos[datos.fecha == time.strftime(timeformat)][variable])
            consumoPasado = consumoPasado + row[variable]
            contador = contador + 1
    if (contador > 0):
        return (consumoActual / contador, consumoPasado / contador)
    else:
        return (0, 0)


def generaResumenCentroVariableSum(centro, datosTotales, datosAnyoAnterior, datosAnyoActual, variable):
    datos = datosAnyoActual[datosAnyoActual["centro"] == centro]
    datos18 = datosAnyoAnterior[datosAnyoAnterior["centro"] == centro]
    consumoActual = 0.0
    consumoPasado = 0.0
    for i, row in datos18.iterrows():
        time = row["fecha"]  # datetime.strptime(row["fecha"], timeformat)
        time = time.replace(year=time.year + 1)
        #datos18.set_value(i, "fecha", time)
        # Se quiere contabilizar sólo aquellos meses para los que se tenga factura en el año en curso
        if (len(datos[datos.fecha == time].index) == 1):  # time.strftime(timeformat)]) == 1):
            # print(datos[datos.fecha == time.strftime("%Y-%m-%d")])
            # print(int(datos[datos.fecha == time.strftime("%Y-%m-%d")]["consumo"]))
            consumoActual = consumoActual + int(datos[datos.fecha == time.strftime(timeformat)][variable])
            consumoPasado = consumoPasado + row[variable]
    return (consumoActual, consumoPasado)


def generarFiguraCentroVariable(centro, datosTotales, datosAnyoAnterior, datosAnyoActual, variable):
    datos = datosAnyoActual[datosAnyoActual["centro"] == centro]
    datos18 = datosAnyoAnterior[datosAnyoAnterior["centro"] == centro]
    # Para superponer los datos del año anterior con el actual
    for i, row in datos18.iterrows():
        time = row["fecha"]  # datetime.strptime(row["fecha"], timeformat)
        time = time.replace(year=time.year + 1)
        time = time - timedelta(days=1)  # para ajustar el cambio de año y que coincidan los días
        # time = time.replace(day=time.day -1 )
        #datos18.set_value(i, "fecha", time.strftime(timeformat))

    fig = px.line(datos, x="fecha", y=variable)
    fig.add_trace(
        go.Line(x=datos18["fecha"], y=datos18[variable], mode="lines", showlegend=True, name="Año anterior"))

    figurahtml = (fig.to_html())
    soup = BeautifulSoup(figurahtml)  # make soup that is parse-able by bs
    divs = soup.findAll('div')

    return divs[0]


def getResumenCadenaVariacion(valorActual, valorPasado, unidad):
    resumenVariable = ""
    resumenVariable = resumenVariable + (
            "El año pasado:" + "{:,}".format(valorPasado) + "; el actual :" + "{:,}".format(
        valorActual) + " " + unidad + "\n")
    if (valorPasado > 0 and valorActual / valorPasado > 1.1):
        resumenVariable = resumenVariable + ("<p class='destacar'>Diferencia " + "{:,}".format(
            valorActual - valorPasado) + "; " + unidad + " lo que supone un " +
                                             "{:.2f}".format(
                                                 valorActual / valorPasado) + " más que el año pasado</p>\n")
    else:
        if (valorPasado > 0):
            resumenVariable = resumenVariable + ("<p>Diferencia " + "{:,}".format(
                valorActual - valorPasado) + "; kwh lo que supone un " +
                                                 "{:.2f}".format(
                                                     valorActual / valorPasado) + " del año pasado</p>\n")
        else:
            resumenVariable = resumenVariable + ("<p>Diferencia " + "{:,}".format(
                valorActual - valorPasado) + " " + unidad + "\n")
    return resumenVariable


def generarResumenCentros(datosTotales, datosAnyoAnterior, datosAnyoActual, periodo):
    for centro in datosAnyoAnterior["centro"].drop_duplicates():
        graficaReactiva = generarFiguraCentroVariable(centro, datosTotales, datosAnyoAnterior, datosAnyoActual, "reactiva")

        (resumenReactivaA, resumenReactivaP) = generaResumenCentroVariableSum(centro, datosTotales, datosAnyoAnterior,
                                                                              datosAnyoActual,
                                                                              "reactiva")
        graficaConsumo = generarFiguraCentroVariable(centro, datosTotales, datosAnyoAnterior, datosAnyoActual,
                                                     "consumo")
        (resumenConsumoA, resumenConsumoP) = generaResumenCentroVariableSum(centro, datosTotales, datosAnyoAnterior,
                                                                            datosAnyoActual,
                                                                            "consumo")
        graficaPotencia = generarFiguraCentroVariable(centro, datosTotales, datosAnyoAnterior, datosAnyoActual,
                                                      "potenciaact")
        (resumenPotenciaA, resumenPotenciaP) = generaResumenCentroVariableMedia(centro, datosTotales, datosAnyoAnterior,
                                                                                datosAnyoActual,
                                                                                "potenciaact")

        graficaPotenciaMax = generarFiguraCentroVariable(centro, datosTotales, datosAnyoAnterior, datosAnyoActual,
                                                         "potenciamax")
        (resumenPotenciaMA, resumenPotenciaMP) = generaResumenCentroVariableMedia(centro, datosTotales,
                                                                                  datosAnyoAnterior,
                                                                                  datosAnyoActual, "potenciamax")
    if (periodo == 'M'):
        graficaCoste = generarFiguraCentroVariable(centro, datosTotales, datosAnyoAnterior, datosAnyoActual,
                                                   "coste")
        (resumenCosteA, resumenCosteP) = generaResumenCentroVariableSum(centro, datosTotales, datosAnyoAnterior,
                                                                        datosAnyoActual,
                                                                        "coste")

        # graficaCO2 = generarFiguraCentroVariable(centro, datosTotales, datosAnyoAnterior, datosAnyoActual,
        #                                               "co2")
        # (resumenCO2A, resumenCO2P) = generaResumenCentroVariable(centro, datosTotales, datosAnyoAnterior,
        #                                                                    datosAnyoActual,
        #                                                                    "co2")

        Html_file = open("output/" + centro + "-" + periodo + ".html", "w")
        Html_file.write("""<html><head>
        
<meta charset="UTF-8">

                       <link rel="stylesheet" href="estilo.css">
                       </head><body>\n""");
        Html_file.write("<h1>Evaluación del centro " + centro + " con frecuencia " + periodo + "</h1>")
        Html_file.write(
            "<p> OBSERVACION: El valor del año anterior ha sido ajustado teniendo en cuenta el cambio de año, mostrará el valor de la misma fecha en el día anterior para que coincidan los días de la semana</p>")
        Html_file.write("<h2>Consumo en kwh</h2>")
        Html_file.write(str(graficaConsumo) + "\n")
        Html_file.write(getResumenCadenaVariacion(resumenConsumoA, resumenConsumoP, "kWh"))

        Html_file.write("<h2>Consumo en rectiva</h2>")
        Html_file.write(str(graficaReactiva) + "\n")
        Html_file.write(getResumenCadenaVariacion(resumenReactivaA, resumenReactivaP, "kVArh"))

        Html_file.write("<h2>Potencia activa media</h2>")
        Html_file.write(str(graficaPotencia) + "\n")
        Html_file.write(getResumenCadenaVariacion(resumenPotenciaA, resumenPotenciaP, "kW"))

        Html_file.write("<h2>Potencia máxima media</h2>")
        Html_file.write(str(graficaPotenciaMax) + "\n")
        Html_file.write(getResumenCadenaVariacion(resumenPotenciaMA, resumenPotenciaMP, "kW"))

    if (periodo == 'M'):
        Html_file.write("<h2>Coste</h2>")
        Html_file.write(str(graficaCoste) + "\n")
        Html_file.write(getResumenCadenaVariacion(resumenCosteA, resumenCosteP, "euros"))

        # Html_file.write("<h2>CO2</h2>")
        # Html_file.write(str(graficaCO2) + "\n")
        # Html_file.write(getResumenCadenaVariacion(resumenCO2A, resumenCO2P, "toneladas CO2"))

        Html_file.write("</body>\n")
        Html_file.write("</html>\n")
        Html_file.close()
        print("Generado " + "output/" + centro + "-" + periodo + ".html")


def generarResumenVariableMedia(datosTotales, datosAnyoAnterior, datosAnyoActual, variable, unidad, periodo):
    fig = px.line(datosTotales, x="fecha", y=variable, line_group="centro",
                  title="Consumo de suministros del último año",
                  color="centro", hover_name="centro")
    # fig.add_line(x=datos2018.date, y=datos2018.consumo)
    # fig.write_html("centros.html")
    # cadenaCentros=fig.to_html(output_type='div', include_plotlyjs=True)
    figurahtml = (fig.to_html())
    soup = BeautifulSoup(figurahtml)  # make soup that is parse-able by bs
    divs = soup.findAll('div')
    # print(get_methods(fig))
    # exit()
    # for centro in datos2018["centro"].drop_duplicates():
    evaluacionCentros = ""

    # for i, row in datosAnyoActual.iterrows():
    # normalizar fecha
    #     time = datetime.strptime(row["fecha"], timeformat)
    #     datosAnyoActual.set_value(i, "fecha", time.strftime(timeformat))
    # datos2018=datos2018.sort_values(by=["centro","fecha"])
    datosCentros = pd.DataFrame([], columns=["centro", "pasado", "actual", "variacion"])
    for centro in datosAnyoAnterior["centro"].drop_duplicates().sort_values(ascending=False):
        difference = 0
        datos = datosAnyoActual[datosAnyoActual["centro"] == centro]
        datos18 = datosAnyoAnterior[datosAnyoAnterior["centro"] == centro]
        consumoActual = 0.0
        consumoPasado = 0.0
        counter = 0
        for i, row in datos18.iterrows():
            time = row["fecha"]  # datetime.strptime(row["fecha"], timeformat)
            time = time.replace(year=time.year + 1)

            # datos18.set_value(i, "fecha", time)
            # Se quiere contabilizar sólo aquellos meses para los que se tenga factura en el año en curso
            if (len(datos[datos.fecha == time].index) == 1):  # time.strftime(timeformat)]) == 1):
                # print(datos[datos.fecha == time.strftime("%Y-%m-%d")])
                # print(int(datos[datos.fecha == time.strftime("%Y-%m-%d")]["consumo"]))
                if (not math.isnan(datos[datos.fecha == time][variable])):
                    consumoActual = consumoActual + int(
                        datos[datos.fecha == time][variable])  # time.strftime(timeformat)][variable])
                consumoPasado = consumoPasado + row[variable]
                counter = counter + 1
                # print(str(consumoPasado))
        #  else:
        #      print ("No encuentro para "+str(time)+ str(len(datos[datos.fecha == time])))
        if (counter > 0):
            consumoActual = consumoActual / counter
            consumoPasado = consumoPasado / counter
        if (consumoPasado > 0 and consumoActual / consumoPasado > 1.1):
            evaluacionCentros = evaluacionCentros + (
                    "<a class='destacar' href='" + centro + "-" + periodo + ".html'>" + centro + " (" + "{:.2f}".format(
                consumoActual / consumoPasado) + "; " + "{:,}".format(
                consumoActual - consumoPasado) + ")</a>\n<br/>")
            datosCentros = datosCentros.append(
                pd.DataFrame([[centro, consumoPasado, consumoActual, consumoActual / consumoPasado]],
                             columns=["centro", "pasado", "actual", "variacion"]))
        else:
            evaluacionCentros = evaluacionCentros + (
                    "<a  href='" + centro + "-" + periodo + ".html'>" + centro + " (" + "{:,}".format(
                consumoActual - consumoPasado) + ")</a>\n<br/>")
            if (consumoPasado > 0):
                datosCentros = datosCentros.append(
                    pd.DataFrame([[centro, consumoPasado, consumoActual, consumoActual / consumoPasado]],
                                 columns=["centro", "pasado", "actual", "variacion"]))
            else:
                datosCentros = datosCentros.append(pd.DataFrame([[centro, consumoPasado, consumoActual, 0]],
                                                                columns=["centro", "pasado", "actual", "variacion"]))

    Html_file = open("output/" + "centros-" + variable + "-" + periodo + ".html", "w")
    Html_file.write("""<html><head>
    
<meta charset="UTF-8">

                <link rel="stylesheet" href="estilo.css">
                </head><body>\n""");
    Html_file.write("<h1>Evaluación de centros atendiendo a " + variable + " y frecuencia " + periodo + "</h1>")
    Html_file.write(str(divs[0]))
    Html_file.write("<h1>Resumen</h1>")
    Html_file.write("<p>")
    Html_file.write("Valor actual (" + unidad + "): " + "{:,}".format(datosCentros["actual"].mean()) +
                    " pasado (" + unidad + "):" + "{:,}".format(datosCentros["pasado"].mean()))
    if (datosCentros["pasado"].mean() > 0):
        Html_file.write(" variación:" + "{:.2f}".format(
            datosCentros["actual"].sum() / datosCentros["pasado"].mean()) + "<br/>")

    Html_file.write("</p>")
    Html_file.write("<p> Los valores aparecen como pares (variación, diferencia), siendo el primero el resultado "
                    "de dividir los valores del año actual entre los del pasado. La 'diferencia' se refiere a la resta"
                    "del valor del año actual menos los del pasado.</p><p> Los centros en rojo denotan variaciones superiores "
                    "a 1.1 (un 10% superior) en los valores del centro.</p>")
    Html_file.write("<div class='columnas'>")
    Html_file.write(evaluacionCentros)
    Html_file.write("</div>")
    Html_file.write("<h1>Centros que empeoran (ordenados por impacto)</h1>")
    datosCentrosEmpeoran = datosCentros[datosCentros["variacion"] > 1].sort_values(by=["variacion"], ascending=False)
    if (len(datosCentrosEmpeoran.index) > 1):
        cadena = ""
        for i, row in datosCentrosEmpeoran.iterrows():
            cadena = cadena + "<a href='" + row["centro"] + "-" + periodo + ".html'>" + row[
                "centro"] + "(" + "{:.2f}".format(
                row["variacion"]) + "," + "{:,}".format(row["actual"] - row["pasado"]) + ")</a>\n<br/>"
        Html_file.write("<p>")
        Html_file.write("Consumo actual (" + unidad + "): " + "{:,}".format(datosCentrosEmpeoran["actual"].mean()) +
                        " pasado (" + unidad + "):" + "{:,}".format(datosCentrosEmpeoran["pasado"].mean()))
        if (datosCentrosEmpeoran["pasado"].mean() > 0):
            Html_file.write(" variación:" + "{:.2f}".format(
                datosCentrosEmpeoran["actual"].mean() / datosCentrosEmpeoran["pasado"].mean()) + "<br/>")

        Html_file.write("</p>")
        Html_file.write("<div class='columnas'>")
        Html_file.write(cadena)
        Html_file.write("</div>")
    else:
        Html_file.write("<p>No empeora ninguno</p>")

    Html_file.write("<h1>Centros que mejoran (ordenados por impacto)</h1>")
    datosCentrosMejoran = datosCentros[datosCentros["variacion"] <= 1].sort_values(by=["variacion"], ascending=False)
    if (len(datosCentrosMejoran.index) > 1):
        cadena = ""
        for i, row in datosCentrosMejoran.iterrows():
            cadena = cadena + "<a href='" + row["centro"] + "-" + periodo + ".html'>" + row[
                "centro"] + "(" + "{:.2f}".format(
                row["variacion"]) + "," + "{:,}".format(row["actual"] - row["pasado"]) + ")</a>\n<br/>"
        Html_file.write("<p>")
        Html_file.write("Valor actual (" + unidad + "): " + "{:,}".format(datosCentrosMejoran["actual"].mean()) +
                        " pasado (" + unidad + "):" + "{:,}".format(datosCentrosMejoran["pasado"].mean()))

        Html_file.write(" variación:" + "{:.2f}".format(
            datosCentrosMejoran["actual"].sum() / datosCentrosMejoran["pasado"].mean()) + "<br/>")
        Html_file.write("</p>")
        Html_file.write("<div class='columnas'>")
        Html_file.write(cadena)
        Html_file.write("</div>")
    else:
        Html_file.write("<p>No mejora ningún centro</p>")
    Html_file.write("</html>\n")
    Html_file.close()
    print("Generado " + "centros-" + variable + "-" + periodo + ".html")


def generarResumenVariableSum(datosTotales, datosAnyoAnterior, datosAnyoActual, variable, unidad, periodo):
    fig = px.line(datosTotales, x="fecha", y=variable, line_group="centro",
                  title="Consumo de suministros del último año",
                  color="centro", hover_name="centro")
    # fig.add_line(x=datos2018.date, y=datos2018.consumo)
    # fig.write_html("centros.html")
    # cadenaCentros=fig.to_html(output_type='div', include_plotlyjs=True)
    figurahtml = (fig.to_html())
    soup = BeautifulSoup(figurahtml)  # make soup that is parse-able by bs
    divs = soup.findAll('div')
    # print(get_methods(fig))
    # exit()
    # for centro in datos2018["centro"].drop_duplicates():
    evaluacionCentros = ""

    # for i, row in datosAnyoActual.iterrows():
    # normalizar fecha
    #     time = datetime.strptime(row["fecha"], timeformat)
    #     datosAnyoActual.set_value(i, "fecha", time.strftime(timeformat))
    # datos2018=datos2018.sort_values(by=["centro","fecha"])
    datosCentros = pd.DataFrame([], columns=["centro", "pasado", "actual", "variacion"])
    for centro in datosAnyoAnterior["centro"].drop_duplicates().sort_values(ascending=False):
        difference = 0
        datos = datosAnyoActual[datosAnyoActual["centro"] == centro]
        datos18 = datosAnyoAnterior[datosAnyoAnterior["centro"] == centro]
        consumoActual = 0.0
        consumoPasado = 0.0
        for i, row in datos18.iterrows():
            time = row["fecha"]  # datetime.strptime(row["fecha"], timeformat)
            time = time.replace(year=time.year + 1)

            # datos18.set_value(i, "fecha", time)
            # Se quiere contabilizar sólo aquellos meses para los que se tenga factura en el año en curso
            if (len(datos[datos.fecha == time].index) == 1):  # time.strftime(timeformat)]) == 1):
                # print(datos[datos.fecha == time.strftime("%Y-%m-%d")])
                # print(int(datos[datos.fecha == time.strftime("%Y-%m-%d")]["consumo"]))
                consumoActual = consumoActual + int(
                    datos[datos.fecha == time][variable])  # time.strftime(timeformat)][variable])
                consumoPasado = consumoPasado + row[variable]
                # print(str(consumoPasado))
        #  else:
        #      print ("No encuentro para "+str(time)+ str(len(datos[datos.fecha == time])))

        if (consumoPasado > 0 and consumoActual / consumoPasado > 1.1):
            evaluacionCentros = evaluacionCentros + (
                    "<a class='destacar' href='" + centro + "-" + periodo + ".html'>" + centro + " (" + "{:.2f}".format(
                consumoActual / consumoPasado) + "; " + "{:,}".format(
                consumoActual - consumoPasado) + ")</a>\n<br/>")
            datosCentros = datosCentros.append(
                pd.DataFrame([[centro, consumoPasado, consumoActual, consumoActual / consumoPasado]],
                             columns=["centro", "pasado", "actual", "variacion"]))
        else:
            evaluacionCentros = evaluacionCentros + (
                    "<a  href='" + centro + "-" + periodo + ".html'>" + centro + " (" + "{:,}".format(
                consumoActual - consumoPasado) + ")</a>\n<br/>")
            if (consumoPasado > 0):
                datosCentros = datosCentros.append(
                    pd.DataFrame([[centro, consumoPasado, consumoActual, consumoActual / consumoPasado]],
                                 columns=["centro", "pasado", "actual", "variacion"]))
            else:
                datosCentros = datosCentros.append(pd.DataFrame([[centro, consumoPasado, consumoActual, 0]],
                                                                columns=["centro", "pasado", "actual",
                                                                         "variacion"]))

    Html_file = open("output/" + "centros-" + variable + "-" + periodo + ".html", "w")
    Html_file.write("""<html><head>

    <meta charset="UTF-8">

                    <link rel="stylesheet" href="estilo.css">
                    </head><body>\n""");
    Html_file.write("<h1>Evaluación de centros atendiendo a " + variable + " y frecuencia " + periodo + "</h1>")
    Html_file.write(str(divs[0]))
    Html_file.write("<h1>Resumen</h1>")
    Html_file.write("<p>")
    Html_file.write("Valor actual (" + unidad + "): " + "{:,}".format(datosCentros["actual"].sum()) +
                    " pasado (" + unidad + "):" + "{:,}".format(datosCentros["pasado"].sum()))
    if (datosCentros["pasado"].sum() > 0):
        Html_file.write(" variación:" + "{:.2f}".format(
            datosCentros["actual"].sum() / datosCentros["pasado"].sum()) + "<br/>")

    Html_file.write("</p>")
    Html_file.write("<p> Los valores aparecen como pares (variación, diferencia), siendo el primero el resultado "
                    "de dividir los valores del año actual entre los del pasado. La 'diferencia' se refiere a la resta"
                    "del valor del año actual menos los del pasado.</p><p> Los centros en rojo denotan variaciones superiores "
                    "a 1.1 (un 10% superior) en los valores del centro.</p>")
    Html_file.write("<div class='columnas'>")
    Html_file.write(evaluacionCentros)
    Html_file.write("</div>")
    Html_file.write("<h1>Centros que empeoran (ordenados por impacto)</h1>")
    datosCentrosEmpeoran = datosCentros[datosCentros["variacion"] > 1].sort_values(by=["variacion"],
                                                                                   ascending=False)
    if (len(datosCentrosEmpeoran.index) > 1):
        cadena = ""
        for i, row in datosCentrosEmpeoran.iterrows():
            cadena = cadena + "<a href='" + row["centro"] + "-" + periodo + ".html'>" + row[
                "centro"] + "(" + "{:.2f}".format(
                row["variacion"]) + "," + "{:,}".format(row["actual"] - row["pasado"]) + ")</a>\n<br/>"
        Html_file.write("<p>")
        Html_file.write("Consumo actual (" + unidad + "): " + "{:,}".format(datosCentrosEmpeoran["actual"].sum()) +
                        " pasado (" + unidad + "):" + "{:,}".format(datosCentrosEmpeoran["pasado"].sum()))
        if (datosCentrosEmpeoran["pasado"].sum() > 0):
            Html_file.write(" variación:" + "{:.2f}".format(
                datosCentrosEmpeoran["actual"].sum() / datosCentrosEmpeoran["pasado"].sum()) + "<br/>")

        Html_file.write("</p>")
        Html_file.write("<div class='columnas'>")
        Html_file.write(cadena)
        Html_file.write("</div>")
    else:
        Html_file.write("<p>No empeora ninguno</p>")

    Html_file.write("<h1>Centros que mejoran (ordenados por impacto)</h1>")
    datosCentrosMejoran = datosCentros[datosCentros["variacion"] <= 1].sort_values(by=["variacion"],
                                                                                   ascending=False)
    if (len(datosCentrosMejoran.index) > 1):
        cadena = ""
        for i, row in datosCentrosMejoran.iterrows():
            cadena = cadena + "<a href='" + row["centro"] + "-" + periodo + ".html'>" + row[
                "centro"] + "(" + "{:.2f}".format(
                row["variacion"]) + "," + "{:,}".format(row["actual"] - row["pasado"]) + ")</a>\n<br/>"
        Html_file.write("<p>")
        Html_file.write("Valor actual (" + unidad + "): " + "{:,}".format(datosCentrosMejoran["actual"].sum()) +
                        " pasado (" + unidad + "):" + "{:,}".format(datosCentrosMejoran["pasado"].sum()))

        Html_file.write(" variación:" + "{:.2f}".format(
            datosCentrosMejoran["actual"].sum() / datosCentrosMejoran["pasado"].sum()) + "<br/>")
        Html_file.write("</p>")
        Html_file.write("<div class='columnas'>")
        Html_file.write(cadena)
        Html_file.write("</div>")
    else:
        Html_file.write("<p>No mejora ningún centro</p>")
    Html_file.write("</html>\n")
    Html_file.close()
    print("Generado " + "centros-" + variable + "-" + periodo + ".html")


def func(x):
    x = ''.join(x.values)
    return x


def simplifica(datosTotales, resamplePeriod):
    if (resamplePeriod == "M"):
        # en este caso hay que quitar todas las entradas en cada centro en las que no haya un mes completo
        # de lo contrario, salen datos incompletos al comparar el muestreo por día vs muestreo por mes
        # pasará lo mismo en el muestreo por hora vs muestreo por día, pero el impacto debería ser menor
        datospordia = datosTotales.groupby(['centro', 'tarifa']).resample("d").sum().reset_index()
        for centro in datospordia["centro"].drop_duplicates():

            datos = datospordia[(datospordia["centro"] == centro) & (
                        (datospordia["tarifa"] == '6.1A') | (datospordia["tarifa"] == '3.1A'))]
            if (len(datos.index) > 0):
                # solo filtra las tarifas para las que tenemos datos diarios
                for mes in range(1, 12):
                    mascarames = datos['fecha'].map(lambda x: x.month == mes)

                    numeroDeAnyosConMismoMes = 2  # hay dos años registrados ahora
                    print(centro + " " + str(mes) + "-- " + str(len(datos[mascarames].index)) + " -- " + str(
                        (monthrange(2019, mes)[1] * 0.8 * numeroDeAnyosConMismoMes)) + " " + str(
                        len(datos[mascarames].index) < (monthrange(2019, mes)[1] * numeroDeAnyosConMismoMes * 0.8)))
                    if (len(datos[mascarames].index) > 0 and len(datos[mascarames].index) < (monthrange(2019, mes)[
                                                                                                 1] * numeroDeAnyosConMismoMes * 0.8)):  # cuenta el número de meses iguales registrados, ahora son 2
                        # TODO: contar el número de años que constan con ese mes
                        # no hay suficientes días en ese mes, da igual el año
                        # se borran en los datos originales las filas correspondientes a ese mes para no crear
                        # disparidad con respecto de las medidas ese día
                        indexNames = datosTotales[
                            (datosTotales['fecha'].dt.month == mes) & (datosTotales['centro'] == centro)].index
                        print("antes:" + str(len(datosTotales.index)))
                        print(str(len(datosTotales[(datosTotales['fecha'].dt.month == mes) & (
                                    datosTotales['centro'] == centro)].index)))
                        print(str(len(datos[mascarames].index)))
                        datosTotales.drop(indexNames, inplace=True)
                        print(str(len(datosTotales[(datosTotales['fecha'].dt.month == mes) & (
                                datosTotales['centro'] == centro)].index)))
                        print("despues " + str(len(datosTotales.index)))
    return datosTotales


def generarTodo(resamplePeriod):
    mes = datetime.today().strftime('%m')
    anyo = datetime.today().strftime('%Y')

    datosTotales = pd.read_csv("datosfiltrados.csv")
    #    datosTotales = datosTotales.drop(datosTotales[datosTotales.coste=='coste'],inplace=True).reset_index()
    datosTotales['fecha'] = pd.to_datetime(datosTotales['fecha'])

    datosTotales.index = datosTotales['fecha']

    # datosTotales=simplifica(datosTotales, resamplePeriod)

    datosTotales = datosTotales.groupby(['centro']).resample(resamplePeriod).agg(
        {"id": "last", "consumo": "sum", "reactiva": "sum", "co2": "sum", "potenciamax": "median",
         "potenciaact": "median", "tarifa": "last", "coste": "last"}).reset_index()
    # datosTotales =datosTotales.reset_index();

    datosTotales = datosTotales.sort_values(by=['fecha'])
    # hay lecturas parciales hasta mes-1 que hacen inconsistentes los datos con frecuencia d y M.
    # por ejemplo, si estamos en octubre, y sólo se tiene el día 1 de septiembre de telelectura
    # la comparación con años anteriores con frecuencia d salen bien, pero no con frecuencia M al tener datos completos
    # el año anterior para el d y M, tener datos completos para d en el actual, pero no para el M.
    # Por eso, hay que pedir datos hasta el día 1 del (mes-1) (no inclusive)
    datosTotales = datosTotales[
        datosTotales['fecha'] < datetime.strptime(r"2019-" + str(int(mes) - 1) + "-01 00:00", timeformat)]

    # Se comparan años porque hay que ver variaciones en las mismas condiciones climáticas
    datosAnyoAnterior = datosTotales[datosTotales['fecha'] < datetime.strptime(r"2019-01-01 00:00", timeformat)]
    datosAnyoAnterior = datosAnyoAnterior[
        datosAnyoAnterior['fecha'] >= datetime.strptime(r"2018-01-01 00:00", timeformat)]
    datosAnyoActual = datosTotales[datosTotales['fecha'] >= datetime.strptime(r"2019-01-01 00:00", timeformat)]

    # Convert that column into a datetime datatype
    # datosAnyoAnterior['fecha'] = pd.to_datetime(datosAnyoAnterior['fecha'])
    # datosAnyoActual['fecha'] = pd.to_datetime(datosAnyoActual['fecha'])
    # datosAnyoAnterior.index = datosAnyoAnterior['fecha']
    # datosAnyoActual.index = datosAnyoActual['fecha']
    # datosAnyoActual=datosAnyoActual.groupby(['centro','tarifa']).resample('M').sum().reset_index()#.agg({'centro':func,'consumo':sum})
    # datosAnyoAnterior=datosAnyoAnterior.groupby(['centro','tarifa']).resample('M').sum().reset_index()

    # generarResumenVariable(datosTotales, datosAnyoAnterior, datosAnyoActual, "co2", "toneladas de CO2", resamplePeriod)
    generarResumenVariableSum(datosTotales, datosAnyoAnterior, datosAnyoActual, "consumo", "kWh", resamplePeriod)
    generarResumenVariableSum(datosTotales, datosAnyoAnterior, datosAnyoActual, "reactiva", "kVArh", resamplePeriod)
    generarResumenVariableMedia(datosTotales, datosAnyoAnterior, datosAnyoActual, "potenciaact", "kW", resamplePeriod)
    generarResumenVariableMedia(datosTotales, datosAnyoAnterior, datosAnyoActual, "potenciamax", "kW", resamplePeriod)
    generarResumenVariableSum(datosTotales, datosAnyoAnterior, datosAnyoActual, "coste", "euros", resamplePeriod)
    generarResumenCentros(datosTotales, datosAnyoAnterior, datosAnyoActual, resamplePeriod)


if __name__ == '__main__':
    timeformat = "%Y-%m-%d %H:%M"
    resamplePeriod = 'M'  # 'Y','M','d', 'h'

    generarTodo("M")
    generarTodo("d")
    generarTodo("h")
