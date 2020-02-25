#!/usr/bin/env python3

from solar.solar_energy import Solar_energy
from solar.input_energy import Input_energy
from config.configurator import Configurator

import matplotlib.pyplot as plt

def analysis_monthly():

    config_solar = Configurator(config_path = 'config/config.yaml', year = 2016) 
    input_solar = Solar_energy(configurator=config_solar, type_data="monthly")

    config_sensor = Configurator(config_path = 'config/config.yaml', year = 2018)
    input_sensor = Input_energy(configurator=config_sensor)

    df_solar = input_solar.extract_json_to_dataframe()[["H(h)_m","month"]]
    df_solar.columns = ['consumo', 'meses']

    print("Irradiation on horizontal plane (kWh/m2/mo)")
    print(df_solar)

    # Realizar calculos con el dataset de la computense
    input_sensor.extract_csv_to_dataframe()

    df_sensor_month = input_sensor.group_by_months().to_frame()
    df_sensor_month.columns = ['consumo']

    df_sensor_month.insert(1, 'meses', range(0, 0 + len(df_sensor_month)))

    print("Consumo sumado de cada mes (kWh)")
    print(df_sensor_month)

    # Mostrar graficamente

    ax = plt.gca()

    df_solar.plot(kind='scatter',x='meses',y='consumo',color='red',ax=ax)
    df_sensor_month.plot(kind='scatter',x='meses',y='consumo',color='blue',ax=ax)
    plt.show()



def analysis_daily():
    return 0

def analysis_hourly():
    return 0


if __name__== "__main__":
    
    print("Start solar analysis...\n\r")

    """ Se puede pedir la informacion de tres formas diferentes:
            - Monthly: Te da la informacion por meses (enero, febrero...) en un solo json
            - Daily: Por mes pero cada mes en un fichero y la media que cada hora del mes.
            - Hourly: Te da todas las horas del anioo.
    """

    analysis_monthly()

    """
        1. Gestionar los tres tipos de anailisis, diario, mensual y anual
        2. Numero de placas solares
        3. Consumo si se tiene baterias o no
    """