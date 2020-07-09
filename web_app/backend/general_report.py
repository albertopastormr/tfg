#!/usr/bin/env python3

from backend.solar.hours_analysis import generate_hours_data as data_hours

import pandas as pd

from bs4 import BeautifulSoup

# Plotly plot
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from backend.config.configurator import Configurator

config_path_sensor = 'backend/config/config_sensor.yaml'


def generate_header(center, date):
    config_sensor = Configurator(config_path=config_path_sensor, center=center, year=date)

    title_text = """
        <h1 style="text-align: center; margin: auto; background-color: rgba(140, 165, 173, 0.733); padding: 2.5%; border:2px solid black">Análisis energético general {} </h1>
    """.format(date)
    subtitle_text = """
            <h2 style="text-align: center; margin: auto; padding: 0.5%;"> {} </h2>
        """.format(config_sensor.get_data_name_center())

    general_text = """
    <div style="width:80%; margin: auto;">
        Es esta página encontrará un informe en el que se estudia a nivel energético cada una de las secciones que haya 
        elegido en el formulario. Se muestra el consumo energético para el centro {} así como información de la energía 
        fotovoltaica obtenida para donde se sitúa geográficamente el centro. Con las diferentes secciones se espera que 
        obtenga toda la información energética que desea. 
        </br></br>
        Destacar que todos los consumos se encuentran en “Kw/h” y “Euros”. 
        
        </br></br>
        Los datos generales dispuestos sobre energia fotovoltaica han sido obtenidos con condiciones óptimas y dos placas solares. 
        Si se desea otras opciones especifíquelo en el formulario previo si no lo ha hecho. Obtendrá el resultado mas abajo.
    </div>
    """.format(config_sensor.get_data_name_center())

    return title_text + "</br>" + subtitle_text + "</br>" + general_text + "</br>"

def generate_analysis_general(center, date):

    df_solar, df_sensor = data_hours.analysis_general(center = center, date = date)

    df_solar.iloc[:, 0] = pd.to_datetime(
        df_solar.iloc[:, 0], format="%Y%m%d:%H%M")
    df_sensor['fecha'] = pd.to_datetime(
        df_sensor['fecha'], format="%Y-%m-%d %H:%M")

    # Solar general report

def generate_general_solar_data(center, date):

    df_solar, _ = data_hours.analysis_general(center = center, date = date)

    df_solar.iloc[:, 0] = pd.to_datetime(
        df_solar.iloc[:, 0], format="%Y%m%d:%H%M")

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[
                [{"type": "table"}],
                [{"type": "scatter"}]
              ]
    )

    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    fig.add_trace(
        go.Table(
            header=dict(
                values=["<b>Date</b>","<b>G(i)</b>","<b>H_sun</b>","<b>T2m</b>","<b>WS10m</b>","<b>Int</b>"],
                line_color='darkslategray',
                fill_color=headerColor,
                align=['left', 'center'],
                font=dict(color='white', size=14)
            ),
            cells=dict(
                values=[df_solar[k].tolist() for k in df_solar.columns[0:]],
                line_color='darkslategray',
                # 2-D list of colors for alternating rows
                fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor] * df_solar.shape[0]],
                align=['left', 'center'],
                font=dict(color='darkslategray', size=12)
            )
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df_solar.iloc[:, 0],
            y=df_solar.iloc[:, 1],
            name="Consume",
            line=dict(color='royalblue', width=3.5)
        ),
        row=2, col=1
        )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1 week", step="day", stepmode="todate"),
                dict(count=1, label="1 month",
                     step="month", stepmode="backward"),
                dict(count=3, label="3 month",
                     step="month", stepmode="backward"),
                dict(count=6, label="6 month",
                     step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    initial_range = [
        df_solar['time'][df_solar.shape[0]-720], df_solar['time'][df_solar.shape[0]-1]
    ]

    fig['layout']['xaxis'].update(range=initial_range)

    fig.update_layout(
        height=750,
        showlegend=False,
        xaxis=dict(
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            rangeslider=dict(),
        ),
    )

    figure_html = (fig.to_html())
    soup = BeautifulSoup(figure_html)
    figure_solar_year = soup.findAll('div')[0]

    return str(figure_solar_year)


def generate_general_sensor_data(center, date):
    _, df_sensor = data_hours.analysis_general(center=center, date=date)

    df_sensor['fecha'] = pd.to_datetime(
        df_sensor['fecha'], format="%Y-%m-%d %H:%M"
    )

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[
                [{"type": "table"}],
                [{"type": "scatter"}]
              ]
    )

    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    fig.add_trace(
        go.Table(
            header=dict(
                values=["<b>Date</b>", "<b>Consume</b>", "<b>Reactive</b>",
                        "<b>CO2</b>", "<b>Max Power</b>", "<b>Active Power</b>",
                        "<b>Rate</b>", "<b>Cost</b>"],
                line_color='darkslategray',
                fill_color=headerColor,
                align=['left', 'center'],
                font=dict(color='white', size=14)
            ),
            cells=dict(
                values=[df_sensor[k].tolist() for k in df_sensor.columns[3:]],
                line_color='darkslategray',
                fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor] * df_sensor.shape[0]],
                align=['left', 'center'],
                font=dict(color='darkslategray', size=12)
            )
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df_sensor['fecha'], 
            y=df_sensor['consumo'], 
            name="Consume"
        ),
        row=2, col=1,
    )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1 week", step="day", stepmode="todate"),
                dict(count=1, label="1 month",
                     step="month", stepmode="backward"),
                dict(count=3, label="3 month",
                     step="month", stepmode="backward"),
                dict(count=6, label="6 month",
                     step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    initial_range = [
        df_sensor['fecha'][df_sensor.shape[0]-720], df_sensor['fecha'][df_sensor.shape[0]-1]
    ]

    fig['layout']['xaxis'].update(range=initial_range)

    fig.update_layout(
        height=750,
        showlegend=False,
        xaxis=dict(
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            rangeslider=dict(),
        ),
    )

    figurahtml = (fig.to_html())
    soup = BeautifulSoup(figurahtml)  # make soup that is parse-able by bs
    figure_input_year = soup.findAll('div')[0]

    return str(figure_input_year)


def sensor_kpi_general(center, date):
    meta_data = data_hours.generate_kpis(center = center, date = date)

    ret_table = """
    <style> table.steelBlueCols { margin: auto; border: 4px solid #555555;    background-color: #555555;    width: 400px;
        text-align: center;    border-collapse: collapse;  }  table.steelBlueCols td, table.steelBlueCols th {    
        border: 1px solid #555555;    padding: 5px 10px;  }  table.steelBlueCols tbody td {    font-size: 12px;    
        font-weight: bold;    color: #FFFFFF;  }  table.steelBlueCols td:nth-child(even) {    background: #398AA4;  }  
        table.steelBlueCols thead {    background: #398AA4;    border-bottom: 10px solid #398AA4;  }  
        table.steelBlueCols thead th {    font-size: 15px;    font-weight: bold;    color: #FFFFFF;    text-align: left;   
         border-left: 2px solid #398AA4;  }  table.steelBlueCols thead th:first-child {    border-left: none;  }    
         table.steelBlueCols tfoot td {    font-size: 13px;  }  table.steelBlueCols tfoot .links {    text-align: right;  }  
         table.steelBlueCols tfoot .links a{    display: inline-block;    background: #FFFFFF;    color: #398AA4;    
         padding: 2px 8px;    border-radius: 5px;  }
    </style>
    """
    ret_table += """
                    </br>
                    <table class="steelBlueCols">
                    <tbody>
                """

    for i in range(len(meta_data)):
        ret_table += "<tr>"
        for j in range(len(meta_data[i])):
            ret_table += "<td>" + str(meta_data[i][j]) + "</td>"
        ret_table += "</tr>"

    ret_table += """
                    </tbody>
                    </table>
                    </br>
                """

    return ret_table


def solar_kpi_general(center, date):
    meta_data = data_hours.generate_kpis(center = center, date = date)

    ret_table = """
    <style> table.steelBlueCols { margin: auto; border: 4px solid #555555;    background-color: #555555;    width: 400px;    text-align: center;    border-collapse: collapse;  }  table.steelBlueCols td, table.steelBlueCols th {    border: 1px solid #555555;    padding: 5px 10px;  }  table.steelBlueCols tbody td {    font-size: 12px;    font-weight: bold;    color: #FFFFFF;  }  table.steelBlueCols td:nth-child(even) {    background: #398AA4;  }  table.steelBlueCols thead {    background: #398AA4;    border-bottom: 10px solid #398AA4;  }  table.steelBlueCols thead th {    font-size: 15px;    font-weight: bold;    color: #FFFFFF;    text-align: left;    border-left: 2px solid #398AA4;  }  table.steelBlueCols thead th:first-child {    border-left: none;  }    table.steelBlueCols tfoot td {    font-size: 13px;  }  table.steelBlueCols tfoot .links {    text-align: right;  }  table.steelBlueCols tfoot .links a{    display: inline-block;    background: #FFFFFF;    color: #398AA4;    padding: 2px 8px;    border-radius: 5px;  }
    </style>
    """
    ret_table += """
                    </br></br>
                    <table class="steelBlueCols">
                    <tbody>
                """

    for i in range(len(meta_data)):
        ret_table += "<tr>"
        for j in range(len(meta_data[i])):
            ret_table += "<td>" + str(meta_data[i][j]) + "</td>"
        ret_table += "</tr>"

    ret_table += """
                    </tbody>
                    </table>
                    </br></br>
                """

    return ret_table


def sensor_active_vs_reactive(center, date):
    _, df_sensor = data_hours.analysis_general(center=center, date=date)

    df_sensor['fecha'] = pd.to_datetime(
        df_sensor['fecha'], format="%Y-%m-%d %H:%M")

    # Create distplot with curve_type set to 'normal'
    fig = go.Figure()

    fig.add_trace(go.Scatter(x= df_sensor['fecha'], y=df_sensor['reactiva'],
                             mode='lines+markers',
                             name='Reactive'))

    fig.add_trace(go.Scatter(x= df_sensor['fecha'], y=df_sensor['potenciamax'] + 10,
                             mode='lines+markers',
                             name='Max'))

    fig.add_trace(go.Scatter(x= df_sensor['fecha'], y=df_sensor['potenciaact'] - 15,
                             mode='lines+markers', name='Active'))

    fig.update_layout(
        height=750,
        xaxis_rangeslider_visible=True,
        xaxis_title="Hours",
        xaxis=dict(
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            rangeslider=dict(),
        ),
    )

    initial_range = [
        df_sensor['fecha'][df_sensor.shape[0] - 720], df_sensor['fecha'][df_sensor.shape[0] - 1]
    ]

    fig['layout']['xaxis'].update(range=initial_range)

    figure_html = (fig.to_html())
    soup = BeautifulSoup(figure_html)  # make soup that is parse-able by bs
    figure_input_year = soup.findAll('div')[0]

    return figure_input_year
