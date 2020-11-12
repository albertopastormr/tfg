#!/usr/bin/env python3

from backend.solar.solar_energy import Solar_energy
from backend.solar.input_energy import Input_energy
from backend.config.configurator import Configurator

config_path_sensor = 'backend/config/config_sensor.yaml'
config_path_solar = 'backend/config/config_solar.yaml'


def analysis_monthly(center, date, num_panels):
    config_solar = Configurator(config_path=config_path_solar, center=center, year=date)
    input_solar = Solar_energy(configurator=config_solar, type_data="monthly", num_panels=num_panels)

    # Ahora esta puesto 2018 para sensor ya que es la prueba de la disponemos
    config_sensor = Configurator(config_path=config_path_sensor, center=center, year=2018)
    input_sensor = Input_energy(configurator=config_sensor)

    input_solar.extract_json_to_dataframe()
    input_sensor.extract_csv_to_dataframe()

    df_sensor_month = input_sensor.group_by(group_by="month", date_format='%m')
    df_sensor_month = df_sensor_month[['fecha', 'consumo', 'coste', 'coste_kw']]

    df_solar_month = input_solar.get_df_solar()[['month', 'H(i_opt)_m']]

    consume_ret = []
    consume_cost_ret = []

    # Calculamos de cada mes en kw y el euros.
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    for index, row in df_sensor_month.iterrows():
        consume = row['consumo'] - (df_solar_month['H(i_opt)_m'].iloc[index] * num_panels)
        consume_cost_ret.append(df_sensor_month['coste_kw'].iloc[index] * consume)
        consume_ret.append(consume)

    return df_sensor_month['consumo'], consume_ret, df_sensor_month['coste'], consume_cost_ret, months
