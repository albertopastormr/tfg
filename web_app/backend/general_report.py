from backend.solar.hours_analysis import generate_hours_data as data_hours
from backend.solar.solar_batterie import Batteries

import numpy as np

import requests
import pprint

import pandas as pd
import xml.etree.ElementTree as et

from bs4 import BeautifulSoup
from dateutil import parser
import math
from calendar import monthrange

import matplotlib.pyplot as plt

# Plotly plot
import plotly.graph_objs as go
import plotly.express as px
import plotly
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_analysis_general(center, date):

    title_text = """
        <h1 style="text-align: center; margin: auto; background-color: cornflowerblue; padding: 2.5%; border:2px solid black">Analisis General Solar</h1>
    """

    description_text = """
    <div style="width:80%; text-align: center; margin: auto;">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam pellentesque hendrerit feugiat. Etiam cursus scelerisque sem, ut congue dolor. Integer eu auctor risus. Sed ultricies ipsum felis, quis elementum leo tempus ut. Curabitur vulputate velit tortor, non laoreet enim maximus ut. Duis sollicitudin neque dolor, vitae tristique enim viverra sed. Duis eget ante vel ante feugiat pretium. Nam porta egestas lectus, ut vehicula ipsum condimentum eu.
        \n\r
        Sed vitae rutrum orci. Nam auctor, est semper maximus ultrices, turpis felis tristique eros, a fermentum dolor tortor quis felis. Donec venenatis metus diam, eget sodales nisl bibendum non. Fusce vitae vehicula dui, in egestas felis. Phasellus nec leo enim. Phasellus et convallis ipsum. Sed semper pellentesque scelerisque. Donec eu ipsum sed ante rhoncus sodales. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur ut dolor aliquam, varius libero feugiat, consectetur nisi. Cras nulla nunc, luctus at sodales at, porttitor sit amet odio.
        \n\r
        Sed lobortis velit ante, nec placerat lorem faucibus vel. Duis in tortor vitae mauris imperdiet sagittis. Aenean convallis enim a elit commodo efficitur. Cras maximus nunc non augue dignissim, at vehicula augue vulputate. Nunc commodo augue lectus, in tristique nibh posuere quis. Sed mi ligula, commodo id tempor quis, maximus malesuada diam. Nulla felis erat, rhoncus at fringilla feugiat, feugiat sit amet turpis. Phasellus commodo neque id leo scelerisque dictum. Curabitur nunc leo, tempor eget tempor eu, sodales tristique nulla. Morbi elit tortor, fringilla ac pellentesque eget, dapibus ac nibh. Aenean quis nunc feugiat, iaculis turpis nec, scelerisque lectus. Morbi tristique pellentesque eros porta luctus.
    </div>
    """

    df_solar, df_sensor = data_hours.analysis_general(center = center, date = date)

    df_solar.iloc[:, 0] = pd.to_datetime(
        df_solar.iloc[:, 0], format="%Y%m%d:%H%M")
    df_sensor['fecha'] = pd.to_datetime(
        df_sensor['fecha'], format="%Y-%m-%d %H:%M")

    # Solar general report

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[
                [{"type": "table"}],
                [{"type": "scatter"}]
              ]
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Date","G(i)","H_sun","T2m","WS10m","Int"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[df_solar[k].tolist() for k in df_solar.columns[0:]],
                align="left")
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df_solar.iloc[:, 0], 
            y=df_solar.iloc[:, 1], 
            name="Consume"),
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

    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="Datos energeticos de placas solares",
    )

    figurahtml = (fig.to_html())
    soup = BeautifulSoup(figurahtml)  # make soup that is parse-able by bs
    figure_solar_year = soup.findAll('div')[0]

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[
                [{"type": "table"}],
                [{"type": "scatter"}]
              ]
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Date", "Consume", "Reactive",
                        "CO2", "Max Power", "Active Power",
                        "Rate", "Cost"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[df_sensor[k].tolist() for k in df_sensor.columns[3:]],
                align="left")
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

    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="Datos energeticos de centro",
    )

    figurahtml = (fig.to_html())
    soup = BeautifulSoup(figurahtml)  # make soup that is parse-able by bs
    figure_input_year = soup.findAll('div')[0]

    return  title_text + "</br>" + description_text + "</br>" + str(figure_solar_year) + str(figure_input_year)

def generate_kpi_general(center, date):
    meta_data = data_hours.generate_kpis(center = center, date = date)

    ret_table = """
    <style> table.steelBlueCols { margin: auto; border: 4px solid #555555;    background-color: #555555;    width: 400px;    text-align: center;    border-collapse: collapse;  }  table.steelBlueCols td, table.steelBlueCols th {    border: 1px solid #555555;    padding: 5px 10px;  }  table.steelBlueCols tbody td {    font-size: 12px;    font-weight: bold;    color: #FFFFFF;  }  table.steelBlueCols td:nth-child(even) {    background: #398AA4;  }  table.steelBlueCols thead {    background: #398AA4;    border-bottom: 10px solid #398AA4;  }  table.steelBlueCols thead th {    font-size: 15px;    font-weight: bold;    color: #FFFFFF;    text-align: left;    border-left: 2px solid #398AA4;  }  table.steelBlueCols thead th:first-child {    border-left: none;  }    table.steelBlueCols tfoot td {    font-size: 13px;  }  table.steelBlueCols tfoot .links {    text-align: right;  }  table.steelBlueCols tfoot .links a{    display: inline-block;    background: #FFFFFF;    color: #398AA4;    padding: 2px 8px;    border-radius: 5px;  }
    </style>
    """
    ret_table += """
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
                """

    return ret_table