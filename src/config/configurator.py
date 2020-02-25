import yaml

"""
    Clases que solo sirve para extraer la informacion del yaml y proveerla al resto de clases.
    Capa intermedia que facilita la extraccion de este fichero de configuracion
"""

class Configurator:
    def __init__(self, config_path = 'config.yaml', year = 2016):
        self.config_path = config_path
        self.year = year
        self.data = self.read_config()

    def read_config(self):
        with open(self.config_path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def get_data_year(self):
        return self.data[self.year]

    def get_where(self, input_type):
        return self.build_dict(self.get_data_year(), key="type").get(input_type)["path"]

    def build_dict(self, seq, key):
        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

if __name__== "__main__":
    config = Configurator(config_path = 'config.yaml', year = 2016)
    print(config.get_data_year(year = 2016))