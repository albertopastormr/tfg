from src.solar.scraper import scraper
from src import solar_analysis


def generate_analysis_month():
    """ Analisis del numero de paneles solares que son necesarios para cubrir la demanda a nivel mensual
    """

    scraper.extract_data_monthly(latitude = "40.568", longitude = "-3.505", start_year=2016, last_year=2016, angle=False)

    solar_analysis.analysis_monthly()

if __name__== "__main__":
    
    print("Start analysis...\n\r")

    generate_analysis_month()

    print("\n\rEnd analysis.\n\r")
