# Third Party Imports
import pandas as pd

def get_unique_sensors(dataframe):
    return dataframe['platform'].unique()