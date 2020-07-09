#!/usr/bin/env python3

from backend.solar.solar_energy import Solar_energy
from backend.solar.input_energy import Input_energy
from backend.config.configurator import Configurator

config_path_sensor = 'backend/config/config_sensor.yaml'
config_path_solar = 'backend/config/config_solar.yaml'

# ANALISYS HOURLY GENERAL

def analysis_general(center, date):

    config_solar = Configurator(config_path = config_path_solar, center = center, year = date)
    input_solar = Solar_energy(configurator=config_solar, type_data="hourly", num_panels=2)

    # Ahora esta puesto 2018 para sensor ya que es la prueba de la disponemos
    config_sensor = Configurator(config_path = config_path_sensor, center = center, year = 2018)
    input_sensor = Input_energy(configurator=config_sensor)

    input_solar.extract_json_to_dataframe()
    input_sensor.extract_csv_to_dataframe()

    return input_solar.get_data(), input_sensor.get_df_sensor()

def generate_kpis(center, date):

    config_solar = Configurator(config_path = config_path_solar, center = center, year = date) 
    input_solar = Solar_energy(configurator=config_solar, type_data="hourly", num_panels=2)

    meta_info = input_solar.get_solar_meta_information()

    return [
            ['latitude','longitude','elevation','radiation_db','meteo_db','slope','azimuth','optimal','technology','peak_power','system_loss'],
            [
                str(meta_info['location']['latitude']),
                str(meta_info['location']['longitude']),
                str(meta_info['location']['elevation']),
                str(meta_info['meteo_data']['radiation_db']),
                str(meta_info['meteo_data']['meteo_db']),
                str(meta_info['mounting_system']['fixed']['slope']['value']),
                str(meta_info['mounting_system']['fixed']['azimuth']['value']),
                str(meta_info['mounting_system']['fixed']['azimuth']['optimal']),
                str(meta_info['pv_module']['technology']),
                str(meta_info['pv_module']['peak_power']),
                str(meta_info['pv_module']['system_loss'])
            ]
        ]


# ANALISYS HOURLY SPECIFIC
def analysis_hourly(center, date, num_panels, solar_batterie=False):

    config_solar = Configurator(config_path = config_path_solar, center = center, year = date)
    input_solar = Solar_energy(configurator=config_solar, type_data="hourly", num_panels=num_panels)

    # Ahora esta puesto 2018 para sensor ya que es la prueba de la disponemos
    config_sensor = Configurator(config_path = config_path_sensor, center = center, year = 2018)
    input_sensor = Input_energy(configurator=config_sensor)

    input_solar.extract_json_to_dataframe()
    input_sensor.extract_csv_to_dataframe()

    consume_ret = []
    extra_information = []
    date_ret = []

    # Agrupamos los dos dataframes por horas
    df_solar_day = input_solar.group_by_hours(is_wattios=True, with_batterie=False)[1:]

    df_sensor_hours = input_sensor.group_by(group_by="day", date_format='%m%d:%H')
    df_sensor_hours = df_sensor_hours[['fecha', 'consumo']]

    # Baterias o no
    if solar_batterie:

        # Calculamos el uso de bateria para cada dia y almacenamos en un array
        for index, row in df_sensor_hours.iterrows():
            consume_ret.append(solar_batterie.calculate_consume_saving(consume=row['consumo'], power_solar_saving=df_solar_day['solar_power'].iloc[index]))

        date_ret = df_sensor_hours['fecha'].values
    else:

        # Calculo cuanta energia segun consumo por hora tenemos que comprar (array)
        # Calculamos al final del dia cuanto pagamos (array)
        acumulation_day = 0
        for index, row in df_sensor_hours.iterrows():
            consume = row['consumo'] - (df_solar_day['solar_power'].iloc[index] * num_panels)
            consume_ret.append(consume)
            acumulation_day = acumulation_day + consume
            if (index % 24) == 1:
                extra_information.append(acumulation_day)
                acumulation_day = 0

        extra_information.append(acumulation_day)
        date_ret = df_sensor_hours['fecha'].values

    return consume_ret, extra_information, date_ret