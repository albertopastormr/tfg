from selenium import webdriver
import pandas as pd

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import glob
import os

import time
from shutil import copyfile

class PVGIS:
    url_pvg = "https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html"
    def __init__(self):
        
        # Load drive with chrome
        self.driver = webdriver.Chrome('src/solar/scraper/chromedriver')

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
        self.driver.find_element_by_id('inputLat').send_keys(latitude)
        self.driver.find_element_by_id('inputLon').send_keys(longitude)
        self.driver.find_element_by_id('btninputLatLon').click()
        time.sleep(1)

    def set_inclination_value(self, angle = 0):
        self.driver.find_element_by_id('angle').clear()
        self.driver.find_element_by_id('angle').send_keys(angle)

    def set_orientation_value(self, angle = 0):
        self.driver.find_element_by_id('aspect').clear()
        self.driver.find_element_by_id('aspect').send_keys(angle)

    def put_option_optimize_slope(self, id_angle="optimalangles"):
        self.driver.find_element_by_id(str(id_angle)).click()

    def change_monthly_data(self):
        self.driver.find_element(By.XPATH, "//a[@href='#MR']").click();

    def change_daily_data(self):
        self.driver.find_element(By.XPATH, "//a[@href='#DR']").click();

    def change_hourly_data(self):
        self.driver.find_element(By.XPATH, "//a[@href='#HR']").click();

    def download_json(self, id_json="pvgriddownloadjson"):
        self.driver.find_element_by_id(str(id_json)).click()
    
    def download_csv(self):
        self.driver.find_element_by_id('pvgriddownloadcsv').click()

    def select_angle(self, angle=0):
        self.driver.find_element_by_id('selectrad').click()
        self.driver.find_element_by_id('mangle').send_keys(str(angle))

    def select_start_year(self, start_year=2016):
        time.sleep(0.2)
        el_last = self.driver.find_element_by_id('mstartyear')
        for option in el_last.find_elements_by_tag_name('option'):
            if option.text == str(start_year):
                option.click()
                break

    def select_end_year(self, last_year=2016):
        time.sleep(0.2)
        el_last = self.driver.find_element_by_id('mendyear')
        for option in el_last.find_elements_by_tag_name('option'):
            if option.text == str(last_year):
                option.click()
                break

    def copy_dataset_downloads_to_project(self):
        time.sleep(1)

        list_of_files = glob.glob('/home/ivanfermena/Downloads/*.json') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)

        copyfile(latest_file, "data/scraper/PVdata_webscraper.json")

    def disconect(self):
        time.sleep(1)
        self.driver.close()


# ------------------- USE CASE ------------------

def extract_data_monthly(latitude = "40.568", longitude = "-3.505", start_year=2016, last_year=2016, angle=False):
    pvgis = PVGIS()

    pvgis.set_latitude_longitude_value(str(latitude), str(longitude))
    pvgis.change_monthly_data()
    pvgis.select_start_year(start_year=start_year)
    pvgis.select_end_year(last_year=last_year)

    if angle:
        pvgis.select_angle(angle)
    else:
        pvgis.put_option_optimize_slope(id_angle="optrad")

    pvgis.download_json(id_json="monthdownloadjson")
    pvgis.copy_dataset_downloads_to_project()

    pvgis.disconect()

if __name__== "__main__":

    extract_data_monthly()