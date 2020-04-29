import yaml

class Configurator:
    """ Clases que solo sirve para extraer la informacion del yaml y proveerla al resto de clases.
        Capa intermedia que facilita la extraccion de este fichero de configuracion
    """
    def __init__(self, config_path = 'src/config/config.yaml', year = 2016):
        self.config_path = config_path
        self.year = year
        self.data = self.read_config()

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
        return self.data[self.year]

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

    def build_dict(self, seq, key):
        """ Genera un diccionario a partir de una secuencia y una clave
        
        Arguments:
            seq {[type]} -- [description]
            key {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))
