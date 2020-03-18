import pandas as pd
import json

"""
    Clase que gestiona toda la informacion destinada y alamacena toda la informacion detallada de la energia solar
    Datos extraidos de la web de la eu
"""

class Solar_energy:
    def __init__(self, configurator, type_data):
        self.config = configurator
        self.type_data = type_data 
        self.df_solar = []

    def extract_json_to_dataframe(self):
        """ Extrae los datos del json y los convierte en un dataframe
        
        Returns:
            Dataframe -- Dataframe con los datos obtenidos del json
        """
        with open(self.config.get_where(input_type = self.type_data)) as json_file:
            self.data = json.load(json_file)
            self.df_solar = pd.DataFrame(self.data["outputs"][self.type_data])
            return self.df_solar

    def get_data(self):
        return self.data

    def get_df_solar(self):
        return self.df_solar

    def group_by_hours(self):
        """ Agrupa por dias y realiza la suma de energia solar
        
        Returns:
            Dataframe -- Suma de consumos degun la fecha en meses
        """
        self.df_solar = self.df_solar[[self.df_solar.columns[0],"time"]]
        self.df_solar.columns = ['solar_power', 'time']

        self.df_solar["time"] = self.df_solar["time"].str[:8]

        self.df_solar = self.df_solar[["time","solar_power"]]

        return self.df_solar.groupby("time")["solar_power"].sum()
        
