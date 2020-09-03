#!/usr/bin/env python3

import pandas as pd
from bs4 import BeautifulSoup
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from backend.config.configurator import Configurator


config_path_sensor = 'backend/config/config_sensor.yaml'


def generate_header(center, date):
    config_sensor = Configurator(config_path=config_path_sensor, center=center, year=date)

    title_text = """
        <h2 style="text-align: center; margin: auto; background-color: rgba(140, 165, 173, 0.733); padding: 0.5%; border:2px solid black">Real-time dashboard - {} </h2>
    """.format(config_sensor.get_data_name_center())

    return title_text + "</br>"


def cal_consume_vs_occupation(df_consume, df_occupation, technical_limit):
    return (((df_consume/df_occupation)*100)/technical_limit) - 100


def generate_real_time(con_person, max_con):

    df = pd.read_csv('./backend/streaming/stream-data-final.csv')

    fig = make_subplots(
        rows=3, cols=6,
        column_widths=[0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        row_heights=[0.5, 0.20, 0.30],
        specs=[
            [{"type": "scatter", "colspan": 3}, None, None, {"type": "scatter", "colspan": 3},None, None],
            [{"type": "indicator", "colspan": 2}, None, {"type": "indicator", "colspan": 2}, None,
                {"type": "indicator", "colspan": 2}, None],
            [{"type": "indicator", "colspan": 6}, None, None, None, None, None],
        ],
        subplot_titles=("Electric Power Demand (kW)", "Occupation (# of people)"),
        horizontal_spacing=0.05,
        vertical_spacing=0.15
    )

    fig.add_trace(
        go.Scatter(
            x=df['fecha'].iloc[-17:],
            y=df['consumo'].iloc[-17:],
            name="Kwh",
            line=dict(color='rgb(49,130,189)', width=3),
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(
            x=df['fecha'].iloc[-17:],
            y=df['num_occupation'].iloc[-17:],
            text=df['num_occupation'].iloc[-17:],
            marker_color='rgb(67,67,67)',
            texttemplate='%{text:s}',
            textposition='outside',

        ),
        row=1, col=4
    )

    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=sum(df['consumo']),
            title={
                "text": "Today's Energy Consumption<br><span style='font-size:0.8em;color:gray'>Accumulated consumption data "
                        "for the current day. </span><br>"
            },
            number={'suffix': " Kwh"},
            delta={'reference': 150, 'relative': True},
            domain={'row': 0, 'column': 1}
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=(df['consumo'].iloc[-1]/df['num_occupation'].iloc[-1]),
            title={
                "text": "Consumption per person<br><span style='font-size:0.8em;color:gray'>Consumption per person of the last data</span><br>"
            },
            number={'suffix': " €"},
            delta={'reference': (df['consumo'].iloc[-2]/df['num_occupation'].iloc[-2]), 'relative': True},
            domain={'row': 0, 'column': 1},
        ),
        row=2, col=3
    )

    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=sum(df['num_occupation']),
            title={
                "text": "Today's Occupation<br><span style='font-size:0.8em;color:gray'>Accumulated occupation data "
                        "for the current day</span><br>"
            },
            number={'suffix': " People"},
            delta={'reference': 80, 'relative': True},
            domain={'row': 0, 'column': 1},
        ),
        row=2, col=5
    )

    fig.add_trace(
        go.Indicator(
            mode="number+gauge+delta",
            value=cal_consume_vs_occupation(df['consumo'].iloc[-1], df['num_occupation'].iloc[-1], float(con_person)),
            title={
                "text": "Percentage of consumption that exceeds the occupation expectations<br>"
                        "<span style='font-size:0.8em;color:gray;'>Red line represents the maximum limit for notice</span><br>"
            },
            number={'suffix': "%"},
            delta={'reference': cal_consume_vs_occupation(df['consumo'].mean(), df['num_occupation'].mean(), 1.5), 'relative': True},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "darkblue"},
                    'steps': [
                       {'range': [0, 20], 'color': "lightgreen"},
                       {'range': [20, 60], 'color': "white"}],
                    'threshold': {'line': {'color': "red", 'width': 4},
                    'thickness': 0.75, 'value': int(max_con)}},
            domain={'row': 0, 'column': 0}
        ),
        row=3, col=1
    )

    fig.update_layout(
        height=820,
        showlegend=False,
        template={'data': {'indicator': [{
            'mode': "number+delta+gauge",
            'delta': {'reference': 100}}]
        }}
    )

    figure_html = (fig.to_html())
    soup = BeautifulSoup(figure_html)
    figure_monitoring_year = soup.findAll('div')[0]

    return str(figure_monitoring_year)
