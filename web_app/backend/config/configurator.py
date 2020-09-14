import yaml

from backend.solar.scraper import scraper

class Configurator:
    """ Clases que solo sirve para extraer la informacion del yaml y proveerla al resto de clases.
        Capa intermedia que facilita la extraccion de este fichero de configuracion
    """
    def __init__(self, center, config_path='src/config/config_solar.yaml', year=2015):
        self.config_path = config_path
        self.year = int(year)
        self.data = self.read_config()
        self.center = int(center)
        self.path_data = './data/'

    def read_config(self):
        """Lee el archivo de configuracion y extrae la informacion de este
        
        Returns:
            json -- Datos de un fichero yaml en formato json
        """
        with open(self.config_path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def get_data_year(self):
        """ Obtiene los datos del yaml de un anyo especificado en el contructor
        
        Returns:
            json -- Coge los datos del yaml especificos de un anyo
        """

        if self.year in self.data[self.center]:
            return self.data[self.center][self.year]
        else:
            return self.insert_year()

    def insert_year(self):
        path_save = self.path_data+"general/"+str(self.year)

        self.data[self.center][self.year] = [{'type': 'hourly', 'directory': 0, 'path': path_save+"/PVdata_webscraper.json", 'format': 'json'}]

        with open(self.config_path, 'w') as f:
            yaml.dump(self.data, f) 

        self.data = self.read_config()

        scraper.extract_data_hourly(path_save=path_save, latitude=self.data[self.center]['latitude'], longitude=self.data[self.center]['latitude'], start_year=str(self.year), last_year=str(self.year), angle=False, aspect=False)

        return self.data[self.center][self.year]

    def get_data_center(self):
        return self.data[self.center]

    def get_data_name_center(self):
        return self.data[self.center]['name']

    def get_where(self, input_type):
        """ Extrae de los datos y de un determinado tipo el path relativo donde esta el dataset
        
        Arguments:
            input_type {String} -- Tipo que se quiere analizar:
                - input: Datos de sensores de edificio
                - daily: Solar diario
                - monthly: Solar mes
                - yearly: Solar anual
        
        Returns:
            String -- Path de donde estan los datos
        """

        return self.build_dict(self.get_data_year(), key="type").get(input_type)["path"]

    def get_where_without_type(self):
        return self.data[self.center]["path"]

    def build_dict(self, seq, key):
        """ Genera un diccionario a partir de una secuencia y una clave
        hourly
        Arguments:
            seq {[type]} -- [description]
            key {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """

        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))
