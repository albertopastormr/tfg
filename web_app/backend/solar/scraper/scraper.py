from selenium import webdriver
import pandas as pd

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import subprocess

import glob
import os

import sys

import time
from shutil import move

class PVGIS:
    """ API. Clase que se encarga de todo la interaccion con la web de PVGIS y scrapea para obtener los datos.
    """
    url_pvg = "https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html"
    def __init__(self):
        
        # Load drive with chrome
        self.driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)

        self.url_data_app = sys.path[0] + "/data/"

        # Access page, accept cookies and reload page
        self.driver.get(self.url_pvg)
        self.driver.find_element_by_link_text('I accept cookies').click()
        self.driver.get(self.url_pvg)

        self.latitude_map = 0
        self.longitude_map = 0
        self.inclination_angle = 0  # (0,90) 
        self.orientation_angle = 0  # (-180,180)
        self.best_optimize_angle = False

    def set_latitude_longitude_value(self, latitude = 0,longitude = 0):
        """ Se dirige a una longitud y latitud de la interfaz
        
        Keyword Arguments:
            latitude {int} -- [description] (default: {0})
            longitude {int} -- [description] (default: {0})
        """
        self.driver.find_element_by_id('inputLat').send_keys(latitude)
        self.driver.find_element_by_id('inputLon').send_keys(longitude)
        self.driver.find_element_by_id('btninputLatLon').click()
        time.sleep(1)

    def set_atributte_value(self, id_angle, angle = 0):
        """Inserta un valor a una determinada propiedad de la interfaz de usuario. Un input
        Uso: Orientacion y Inclinacion
        
        Arguments:
            id_angle {[type]} -- [description]
        
        Keyword Arguments:
            angle {int} -- [description] (default: {0})
        """
        self.driver.find_element_by_id(id_angle).clear()
        self.driver.find_element_by_id(id_angle).send_keys(angle)

    def put_option_optimize_slope(self, id_angle="optimalangles"):
        """
        
        Keyword Arguments:
            id_angle {str} -- [description] (default: {"optimalangles"})
        """
        self.driver.find_element_by_id(str(id_angle)).click()

    def change_type_analysis_data(self, type_changed):
        """ Cambia a la opcion de analisis:
            - Horas: '#HR'
            - Diario: '#DR'
            - Mensual: '#MR'
        """
        self.driver.find_element(By.XPATH, '//a[@href="'+ type_changed + '"]').click();

    def download_json(self, id_json="pvgriddownloadjson"):
        """ Descarga el json a la carpeta de descargas
        """
        self.driver.find_element_by_id(str(id_json)).click()
    
    def download_csv(self, id_csv='pvgriddownloadcsv'):
        """ Descarga el csv a la carpeta de descargas
        """
        self.driver.find_element_by_id(str(id_csv)).click()

    def select_angle(self, id_select="selectrad", id_angle="mangle" ,angle=0):
        """ Selecciona la opcion de angulo y le inserta el que se quiera.
        
        Keyword Arguments:
            id_select {str} -- [description] (default: {"selectrad"})
            id_angle {str} -- [description] (default: {"mangle"})
            angle {int} -- [description] (default: {0})
        """
        self.driver.find_element_by_id(id_select).click()
        self.driver.find_element_by_id(id_angle).send_keys(str(angle))

    def select_start_year(self, id_type='mstartyear', start_year=2016):
        """ Selecciona dentro de las opciones el anyo que quieras como inicio
        
        Keyword Arguments:
            id_type {str} -- [description] (default: {'mstartyear'})
            start_year {int} -- [description] (default: {2016})
        """
        time.sleep(0.2)
        el_last = self.driver.find_element_by_id(id_type)
        for option in el_last.find_elements_by_tag_name('option'):
            if option.text == str(start_year):
                option.click()
                break

    def select_end_year(self, id_type='mendyear' ,last_year=2016):
        """ Selecciona dentro de las opciones el anyo que quieras como final
        
        Keyword Arguments:
            id_type {str} -- [description] (default: {'mendyear'})
            last_year {int} -- [description] (default: {2016})
        """
        time.sleep(0.2)
        el_last = self.driver.find_element_by_id(id_type)
        for option in el_last.find_elements_by_tag_name('option'):
            if option.text == str(last_year):
                option.click()
                break

    def copy_dataset_downloads_to_project(self, path_save):
        """Copia el ultimo archivo descargado dentro de la carpeta del proyecto
        """
        time.sleep(2)

        year_directory = sys.path[0] + path_save[1:]

        file_list = [f for f in os.listdir(self.url_data_app) if f.endswith('.json')]

        time.sleep(1)

        if not os.path.exists(year_directory):
            os.mkdir(year_directory)

        move(self.url_data_app + file_list[0], year_directory +"/PVdata_webscraper.json")

    def disconect(self):
        """Desconecta el driver del scraper. Cierra navegador.
        """
        time.sleep(1)
        self.driver.close()


# ------------------- USE CASE ------------------

def extract_data_monthly(path_save, latitude = "40.568", longitude = "-3.505", start_year=2016, last_year=2016, angle=False):
    """ Realiza el caso de uso que obtienen el numero de paneles solares necesarios para suplir el consumo
    
    Keyword Arguments:
        latitude {str} -- [description] (default: {"40.568"})
        longitude {str} -- [description] (default: {"-3.505"})
        start_year {int} -- [description] (default: {2016})
        last_year {int} -- [description] (default: {2016})
        angle {bool} -- [description] (default: {False})
    """
    pvgis = PVGIS()

    pvgis.set_latitude_longitude_value(str(latitude), str(longitude))
    pvgis.change_type_analysis_data(type_changed="#MR")
    pvgis.select_start_year(id_type='mstartyear', start_year=start_year)
    pvgis.select_end_year(id_type='mendyear', last_year=last_year)

    if angle:
        pvgis.select_angle(angle)
    else:
        pvgis.put_option_optimize_slope(id_angle="optrad")

    pvgis.download_json(id_json="monthdownloadjson")
    pvgis.copy_dataset_downloads_to_project(path_save = path_save)

    pvgis.disconect()

def extract_data_hourly(path_save ,latitude = "40.568", longitude = "-3.505", start_year=2016, last_year=2016, angle=False, aspect=False):

    pvgis = PVGIS()

    pvgis.set_latitude_longitude_value(str(latitude), str(longitude))
    pvgis.change_type_analysis_data(type_changed="#HR")
    pvgis.select_start_year(id_type='hstartyear', start_year=start_year)
    pvgis.select_end_year(id_type='hendyear', last_year=last_year)

    if angle & aspect:
        pvgis.set_atributte_value(id_angle="hourlyangle", angle = angle)
        pvgis.set_atributte_value(id_angle="hourlyaspect", angle = aspect)
    else:
        pvgis.put_option_optimize_slope(id_angle="hourlyoptimalangles")

    pvgis.download_json(id_json="hourlydownloadjson")
    pvgis.copy_dataset_downloads_to_project(path_save = path_save)

    pvgis.disconect()

