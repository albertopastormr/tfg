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
        """ Extrae los datos del csv y los convierte en un dataframe
        
        Returns:
            Dataframe -- Dataframe con los datos obtenidos del csv
        """
        with open(self.config.get_where(input_type = self.type_data)) as csv_file:
            self.df_sensor = pd.read_csv(csv_file) 

    def get_df_sensor(self):
        return self.df_sensor

    def group_by(self, group_by="month"):
        """ Agrupa por lo que le indiquese en el argumento y realiza la suma del consumo
        
        Keyword Arguments:
            group_by {str} -- ES el termino por el que agrupa la fecha (default: {"month"})
            - "month"
            - "hour"
            - "day"
        Returns:
            Dataframe -- Suma de consumos degun la fecha en meses
        """
        if group_by is "month":
            self.df_sensor['fecha'] = pd.to_datetime(self.df_sensor['fecha']).dt.month
        else:
            self.df_sensor['fecha'] = pd.to_datetime(self.df_sensor['fecha']).dt.strftime('%m%d')

        return self.df_sensor.groupby("fecha")["consumo"].sum().reset_index()
