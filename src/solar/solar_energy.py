import pandas as pd
import json

"""
    Clase que gestiona toda la informacion destinada y alamacena toda la informacion detallada de la energia solar
    Datos extraidos de la web de la eu
"""

class Solar_energy:
    def __init__(self, configurator, type_data, num_panels=1):
        self.config = configurator
        self.type_data = type_data 
        self.df_solar = []
        self.num_panels = num_panels

    def extract_json_to_dataframe(self):
        """ Extrae los datos del json y los convierte en un dataframe
        
        Returns:
            Dataframe -- Dataframe con los datos obtenidos del json
        """
        with open(self.config.get_where(input_type = self.type_data)) as json_file:
            self.data = json.load(json_file)
            self.df_solar = pd.DataFrame(self.data["outputs"][self.type_data])
            self.data = self.df_solar

    def get_data(self):
        return self.data

    def get_df_solar(self):
        return self.df_solar

    def group_by_hours(self, is_wattios=False, with_batterie=True):
        """ Agrupa por dias y realiza la suma de energia solar
        
        Returns:
            Dataframe -- Suma de consumos degun la fecha en meses
        """

        G_columns = [col for col in self.df_solar.columns if 'G' in col]
        self.df_solar = self.df_solar[[G_columns[0],"time"]]

        self.df_solar.columns = ['solar_power', 'time']

        self.df_solar["fecha"] = self.df_solar["time"].str[4:8] if with_batterie else self.df_solar["time"].str[4:11]

        self.df_solar = self.df_solar[["fecha","solar_power"]]

        self.df_solar['solar_power'] = self.df_solar['solar_power'].apply(lambda x: x*(self.num_panels/1000)) if is_wattios else self.df_solar['solar_power'].apply(lambda x: x*self.num_panels)
        
        return self.df_solar.groupby("fecha")["fecha","solar_power"].sum().reset_index()
        
