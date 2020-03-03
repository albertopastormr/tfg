from selenium import webdriver
import pandas as pd

class PVGIS:
    def __init__(self):
        
        # Load drive with chrome
        self.driver = webdriver.Chrome('./chromedriver')

        # Access page, accept cookies and reload page
        self.driver.get('https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html')
        self.driver.find_element_by_link_text('I accept cookies').click()
        self.driver.get('https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html')

        self.latitude_map = 0
        self.longitude_map = 0
        self.inclination_angle = 0  # (0,90) 
        self.orientation_angle = 0  # (-180,180)
        self.best_optimize_angle = False

    def set_latitude_longitude_value(self, latitude = 0,longitude = 0):
        self.driver.find_element_by_id('inputLat').send_keys(latitude)
        self.driver.find_element_by_id('inputLon').send_keys(longitude)
        self.driver.find_element_by_id('btninputLatLon').click()

    def set_inclination_value(self, angle = 0):
        self.driver.find_element_by_class_name('angle').send_keys(angle)

    def set_orientation_value(self, angle = 0):
        self.driver.find_element_by_id('aspect').send_keys(angle)
    
if __name__== "__main__":
    pvgis = PVGIS()
    pvgis.set_latitude_longitude_value(latitude = "40.133", longitude = "-3.779")
    pvgis.set_inclination_value(angle = 45)
    pvgis.set_orientation_value(angle = 100)
