#!/usr/bin/env python3

from backend.solar.solar_energy import Solar_energy
from backend.solar.input_energy import Input_energy
from backend.config.configurator import Configurator

config_path_sensor = 'backend/config/config_sensor.yaml'
config_path_solar = 'backend/config/config_solar.yaml'


def analysis_monthly(center, date, num_panels):
    config_solar = Configurator(config_path=config_path_solar, center=center, year=date)
    input_solar = Solar_energy(configurator=config_solar, type_data="month", num_panels=num_panels)

    # Ahora esta puesto 2018 para sensor ya que es la prueba de la disponemos
    config_sensor = Configurator(config_path=config_path_sensor, center=center, year=2018)
    input_sensor = Input_energy(configurator=config_sensor)

    input_solar.extract_json_to_dataframe()
    input_sensor.extract_csv_to_dataframe()

    df_sensor_month = input_sensor.group_by(group_by="month", date_format='%m')
    df_sensor_month = df_sensor_month[['fecha', 'consumo']]

    return str(df_sensor_month)
