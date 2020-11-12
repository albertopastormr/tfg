class Batteries:
    def __init__(self, number_serie=0, power=100, min_discharging_percent=50):
        """[summary]
        
        Keyword Arguments:
            number_serie {int} -- [description] (default: {0})
            power {int} -- Kw/h (default: {100})
            min_discharging_percent {int} -- [description] (default: {50})
        """
        self.number_serie = number_serie
        self.power = power
        self.min_discharging_percent = min_discharging_percent
        self.energy_save = 0
        # Maxima energia almacenaje en baterias
        self.power_max_saving = (self.number_serie * self.power)
        #self.power_min_saving = self.power_max_saving * (float(100 - self.min_discharging_percent) / 100)
        self.power_min_saving = self.power_max_saving * (self.min_discharging_percent / 100)

    def available_save_energy(self):
        return 0 if self.power_min_saving >= self.energy_save else self.energy_save - self.power_min_saving

    def calculate_consume_saving(self, consume, power_solar_saving):
        """ Calcula el consumo que es necesario con la configuracion de bateria y lo que tiene almacenada
        
        Arguments:
            consume {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """

        if consume > power_solar_saving:
            energy_relative = consume - power_solar_saving
            if energy_relative <= self.available_save_energy():
                self.energy_save = self.energy_save - energy_relative
                return 0
            else:
                self.energy_save = self.energy_save - self.available_save_energy()
                return energy_relative - self.available_save_energy()
        else:
            energy_surplus = power_solar_saving - consume
            self.energy_save = self.power_max_saving \
                if energy_surplus + self.energy_save >= self.power_max_saving \
                else energy_surplus + self.energy_save

            return 0


if __name__ == "__main__":
    bt = Batteries(number_serie=2, power=80, min_discharging_percent=50)
    print(bt.calculate_consume_saving(consume=200, power_solar_saving=200))
