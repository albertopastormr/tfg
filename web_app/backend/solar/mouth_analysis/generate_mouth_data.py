#!/usr/bin/env python3

from backend.solar.solar_energy import Solar_energy
from backend.solar.input_energy import Input_energy
from backend.solar.solar_batterie import Batteries
from backend.config.configurator import Configurator

import pandas as pd

import matplotlib.pyplot as plt

config_path = 'backend/config/config.yaml'

# TODO Mejorar metodo para que realice un analisis mas generico. MUY SUCIO - REFACTORIZAR
def analysis_monthly():

    config_solar = Configurator(config_path = 'src/config/config.yaml', year = 2016) 
    input_solar = Solar_energy(configurator=config_solar, type_data="monthly")

    config_sensor = Configurator(config_path = 'src/config/config.yaml', year = 2018)
    input_sensor = Input_energy(configurator=config_sensor)

    df_solar = input_solar.extract_json_to_dataframe().get_data()

    df_solar = input_solar.extract_json_to_dataframe()[[df_solar.columns[0],"month"]]
    df_solar.columns = ['consumo', 'meses']
    df_solar['meses'] = pd.Series(range(0,12))

    print("Irradiation on horizontal plane (kWh/m2/mo)")
    print(df_solar)

    # Realizar calculos con el dataset de la computense
    input_sensor.extract_csv_to_dataframe()

    df_sensor_month = input_sensor.group_by(group_by="month").to_frame()
    df_sensor_month.columns = ['consumo']

    df_sensor_month.insert(1, 'meses', range(0, 0 + len(df_sensor_month)))

    print("Consumo sumado de cada mes (kWh)")
    print(df_sensor_month)

    # Mostrar graficamente el consumo del panel y total input

    ax = plt.gca()

    df_solar.plot(kind='scatter',x='meses',y='consumo',color='red',ax=ax)
    df_sensor_month.plot(kind='scatter',x='meses',y='consumo',color='blue',ax=ax)
    # plt.show()

    num_panels = 0
    array_num_panels = []
    dif_cosume_with_panels = []

    # Conocer cuantas placas solares harian falta para cubrir el consumo. 
    # Cubrir lo que sobre con electricidad contratada
    for index, value_consume in df_solar.iterrows():
        num_panels = (df_sensor_month['consumo'].loc[[index+1]] // value_consume['consumo']).item()
        array_num_panels.append(num_panels * value_consume['consumo'])
        dif_cosume_with_panels.append(df_sensor_month['consumo'].loc[[index+1]].item() - array_num_panels[index])

    df_result = pd.DataFrame(array_num_panels)

    for i, dif in enumerate(dif_cosume_with_panels):
        plt.text(i, array_num_panels[i], dif)

    plt.plot(df_result, color='yellow')
    plt.show()