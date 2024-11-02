
from ._load_data import load_csv_data
COVARIATE_COLUMNS = ['latitude', 'longitude', 'date', 'sea_water_temperature', 'platform']

file ='.\waterTemp_sensorData\COAPS-N7_combined.csv'

def upload_csv_data():

    df = load_csv_data(file, COVARIATE_COLUMNS)
    return df
