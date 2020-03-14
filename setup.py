# La idea es que esta clase este configurada para lanzar todos los informes o generar un menu que puedas escoger el informe determinado
from src.solar.scraper import scraper
from src import solar_analysis

if __name__== "__main__":
    
    print("Start analysis...\n\r")

    # 1. Scraper que coja los valores segun le digo por entrada
    #  [tipo(mensual)] [Cordenadas] [start-year] [last-yangleear] [angle(if null optimun angle)]
    scraper.extract_data_monthly()

    solar_analysis.analysis_monthly()

    print("End analysis.\n\r")
