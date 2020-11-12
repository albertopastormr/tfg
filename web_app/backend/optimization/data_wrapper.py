import json
from datetime import datetime
import pandas as pd

# sensor data
#df = pd.read_csv('2019_input_sensor.csv', parse_dates=['fecha'])
#df['fecha'] = pd.to_datetime(df['fecha']).dt.date
#
#
## irradiance data
#with open('PVdata_webscraper.json') as f:
#  data = json.load(f)