#!/usr/bin/python3
# encoding: utf-8

from src.solar.scraper import scraper
from src import solar_analysis
from src.solar.solar_batterie import Batteries

from src.utils.generate_view import create_inform

import numpy as np

import requests
import pprint
from datetime import *
from dateutil.relativedelta import *
import plotly.graph_objects as go
import pandas as pd
import xml.etree.ElementTree as et
import plotly.graph_objs as go
import plotly.express as px
import plotly
import plotly.io as pio
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from dateutil import parser
import math
from calendar import monthrange

import matplotlib.pyplot as plt

def generate_analysis_month():
    """ Analisis del numero de paneles solares que son necesarios para cubrir la demanda a nivel mensual
    """

    scraper.extract_data_monthly(latitude = "40.568", longitude = "-3.505", start_year=2016, last_year=2016, angle=False)

    solar_analysis.analysis_monthly()

def generate_analysis_hours():
    """ Comparacion por horas de la energia fotovoltaica y el consumo de un determinado lugar, realizando dos tipo de analisis:
            - Disponemos de baterias: De esta forma somos capaces de utilizar la energia sobrante electrica para cuando se necesite
            - No disponemos de baterias: Obtenemos un analisis por hora de coste y cuanto cubrimos por energia solar. 
    """

    #scraper.extract_data_hourly(latitude = "40.568", longitude = "-3.505", start_year=2010, last_year=2010)

    bt = Batteries(number_serie=2, power=80, min_discharging_percent=0)

    #solar_analysis.analysis_hourly(solar_batterie = bt)
    consume_ret, extra_information, dates = solar_analysis.analysis_hourly(solar_batterie = False)

    date_day=[]
    for hour in dates:
        if hour[5:8] == "00":
            date_day.append('{}:00'.format(hour[0:4]))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=consume_ret, name="Consume"))
    fig.add_trace(go.Scatter(x=date_day, y=extra_information, name="Consume"))

    fig.update_layout(title_text='Time Series with Rangeslider', xaxis_rangeslider_visible=True, xaxis_title="Hours", yaxis_title="Consume (Kw/h)")

    #plotly.offline.plot(fig, filename='output/solar/solar.html') 

    figurahtml = (fig.to_html())
    soup = BeautifulSoup(figurahtml)  # make soup that is parse-able by bs
    divs = soup.findAll('div')

    return divs[0]

if __name__== "__main__":
    create_inform(str(generate_analysis_hours()))