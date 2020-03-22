import pandas as pd
import json

class Batteries:
    def __init__(self, number_serie=0, power=100, min_discharging_percent=50):
        self.number_serie = number_serie
        self.power = power
        self.min_discharging_percent = min_discharging_percent

    def calculate_consume_saving(self, consume, power_solar_saving):
        """ Calcula el consumo que es necesario con la configuracion d ebateria y lo que tiene almacenada
        
        Arguments:
            consume {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """

        power_max_saving = (self.number_serie * self.power)

        power_max_saving = power_max_saving if (power_max_saving <= power_solar_saving) else power_solar_saving

        real_power = power_max_saving * (float(100 - self.min_discharging_percent)/100)

        return 0 if real_power >= consume else consume - real_power 

if __name__== "__main__":

    bt = Batteries(number_serie=2, power=80, min_discharging_percent=50)

    print(bt.calculate_consume_saving(consume=200, power_solar_saving=200))
