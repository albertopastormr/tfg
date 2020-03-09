from selenium import webdriver
import pandas as pd

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import time
from shutil import copyfile

class PVGIS:
    url_pvg = "https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html"
    def __init__(self):
        
        # Load drive with chrome
        self.driver = webdriver.Chrome('./chromedriver')

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

    def put_option_optimize_slope(self):
        self.driver.find_element_by_id('optimalangles').click()

    def change_monthly_data(self):
        self.driver.find_element(By.XPATH, "//a[@href='#MR']").click();

    def change_daily_data(self):
        self.driver.find_element(By.XPATH, "//a[@href='#DR']").click();

    def change_hourly_data(self):
        self.driver.find_element(By.XPATH, "//a[@href='#HR']").click();

    def download_json(self):
        self.driver.find_element_by_id('pvgriddownloadjson').click()
    
    def download_csv(self):
        self.driver.find_element_by_id('pvgriddownloadcsv').click()

    # TODO RELATIVE PATH
    def copy_dataset_downloads_to_project(self):
        time.sleep(1)
        copyfile("/home/ivanfermena/Downloads/PVdata_40.133_-3.779_SA_crystSi_1kWp_14_36deg_-2deg.json", "../../../data/scraper/PVdata_40.133_-3.779_SA_crystSi_1kWp_14_36deg_-2deg.json")


if __name__== "__main__":
    pvgis = PVGIS()
    pvgis.set_latitude_longitude_value(latitude = "40.133", longitude = "-3.779")
    
    pvgis.set_inclination_value(angle = '45')
    
    pvgis.set_orientation_value(angle = '100')

    pvgis.put_option_optimize_slope()

    # pvgis.change_monthly_data()

    pvgis.download_json()

    pvgis.copy_dataset_downloads_to_project()
