import pandas as pd

"""
    Clase que gestina toda la informacion relativa a los datos locales y dados por los sensores de la ucm
"""

class Input_energy:
    def __init__(self, configurator):
        self.config = configurator
        self.type_data = "input"
        self.df_sensor = []

    def extract_csv_to_dataframe(self):
        # Limpiamos los datos
        with open(self.config.get_where(input_type = self.type_data)) as csv_file:
            self.df_sensor = pd.read_csv(csv_file) 

    def get_df_sensor(self):
        return self.df_sensor

    def group_by_months(self):
        self.df_sensor['fecha'] = pd.to_datetime(self.df_sensor['fecha']).dt.month

        self.df_sensor = self.df_sensor[["fecha","consumo"]]

        return self.df_sensor.groupby("fecha")["consumo"].sum()
