from src.solar.scraper import scraper
from src import solar_analysis
from src.solar.solar_batterie import Batteries


def generate_analysis_month():
    """ Analisis del numero de paneles solares que son necesarios para cubrir la demanda a nivel mensual
    """

    scraper.extract_data_monthly(latitude = "40.568", longitude = "-3.505", start_year=2016, last_year=2016, angle=False)

    solar_analysis.analysis_monthly()

def generate_analysis_hours():
    """ Comparacion por horas de la energia fotovoltaica y el consumo de un determinado lugar, realizando dos tipo de analisis:
            - Disponemos de baterias: De esta forma somos capaces de utilizar la energia sobrante electrica para cuando se necesite
            - No disponemos de baterias: Obtenemos un analisis por hora de coste y cuanto cubrimos por energia solar. 
    """

    #scraper.extract_data_hourly(latitude = "40.568", longitude = "-3.505", start_year=2010, last_year=2010)

    bt = Batteries(number_serie=2, power=80, min_discharging_percent=0)

    #solar_analysis.analysis_hourly(solar_batterie = bt)
    solar_analysis.analysis_hourly(solar_batterie = False)

if __name__== "__main__":
    
    print("Start analysis...\n\r")

    #generate_analysis_month()

    generate_analysis_hours()

    print("\n\rEnd analysis.\n\r")
