#!/usr/bin/env python3

from solar.solar_energy import Solar_energy
from solar.input_energy import Input_energy
from solar.solar_batterie import Batteries
from config.configurator import Configurator

import pandas as pd

import matplotlib.pyplot as plt

# TODO Mejorar metodo para que realice un analisis mas generico. MUY SUCIO - REFACTORIZAR
def analysis_monthly():

    config_solar = Configurator(config_path = 'src/config/config.yaml', year = 2016) 
    input_solar = Solar_energy(configurator=config_solar, type_data="monthly")

    config_sensor = Configurator(config_path = 'src/config/config.yaml', year = 2018)
    input_sensor = Input_energy(configurator=config_sensor)

    df_solar = input_solar.extract_json_to_dataframe()

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

def analysis_daily():
    return 0

def analysis_hourly(solar_batterie=False):

    config_solar = Configurator(config_path = 'src/config/config.yaml', year = 2016) 
    input_solar = Solar_energy(configurator=config_solar, type_data="hourly", num_panels=2)

    config_sensor = Configurator(config_path = 'src/config/config.yaml', year = 2018)
    input_sensor = Input_energy(configurator=config_sensor)

    input_solar.extract_json_to_dataframe()
    input_sensor.extract_csv_to_dataframe()

    consume_ret = []
    extra_information = []
    date_ret = []

    # Baterias o no
    if solar_batterie:

        # Agrupamos por dia la energia fotovoltaica obtenida
        df_solar_day = input_solar.group_by_hours(is_wattios=True, with_batterie=True)
        #print(df_solar_day)

        # Agrupamos el consumo por dia
        df_sensor_hours = input_sensor.group_by(group_by="day")
        df_sensor_hours = df_sensor_hours[['fecha','consumo']]
        #print(df_sensor_hours.columns.values)

        # Calculamos el uso de bateria para cada dia y almacenamos en un array

        for index, row in df_sensor_hours.iterrows():
            consume_ret.append(solar_batterie.calculate_consume_saving(consume=row['consumo'], power_solar_saving=df_solar_day['solar_power'].iloc[index]))

    else:

        # Agrupamos los dos dataframes por horas
        df_solar_day = input_solar.group_by_hours(is_wattios=True, with_batterie=False)[1:]

        df_sensor_hours = input_sensor.group_by(group_by="day",date_format='%m%d:%H')
        df_sensor_hours = df_sensor_hours[['fecha','consumo']]

        # Calculo cuanta energia segun consumo por hora tenemos que comprar (array)
        # Calculamos al final del dia cuanto pagamos (array)
        acumulation_day = 0
        for index, row in df_sensor_hours.iterrows():
            consume = row['consumo'] - df_solar_day['solar_power'].iloc[index]
            consume_ret.append(consume)
            acumulation_day = acumulation_day + consume
            if (index % 24) == 1:
                extra_information.append(acumulation_day)
                acumulation_day = 0

        extra_information.append(acumulation_day)
        date_ret = df_sensor_hours['fecha'].values

    return consume_ret, extra_information, date_ret

if __name__== "__main__":
    
    print("Start solar analysis...\n\r")

    """ Se puede pedir la informacion de tres formas diferentes:
            - Monthly: Te da la informacion por meses (enero, febrero...) en un solo json
            - Daily: Por mes pero cada mes en un fichero y la media que cada hora del mes.
            - Hourly: Te da todas las horas del anio.
    """

    # 1 Numero de placas solares por mes para compensar la mayoria del gasto y cuanto tienes que pagar de electricidad
    #   - ? Interesante el poder meterle valores de inclinacion, altura... a la placa
    analysis_monthly()

    # 2 Mejor configuracion de grados, colocacion, altura... de la placa para maximizar la energia fotovoltaica
    
    
    # 3 Selecciona un mes o ALL, con baterias o no, cuantas placas solares y te de el consumo por dia segun mes que tienes que pagar
    #   - ? Interesante el saber con una configuracion nuestra o mejor configuracion de placa solar