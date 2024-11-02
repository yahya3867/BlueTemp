"""The blueprint API route for all public endpoints"""
# Python Standard Library Imports
from datetime import datetime
import os

# Python Third Party Imports
from flask import Blueprint, render_template, request

# Local Library Imports
from .database import get_db
from lib.process import upload_csv_data, load_csv_data, get_unique_sensors
from lib.database.model import SensorDevice

# Creating the blueprint route for Public
PUBLIC = Blueprint(name="public", import_name=__name__, template_folder="/templates")


@PUBLIC.route("/", methods=["GET", "POST"])
@PUBLIC.route("/home", methods=["GET", "POST"])
def homepage():
    """API ENDPOINT
    The endpoint for rendering the homepage

    Returns:
        render_template: Renders the homepage/home
        html
    """
<<<<<<< Updated upstream
    return render_template("homepage/home.html")


@PUBLIC.route("/getPredictionBySensor", methods=["GET", "POST"])
def get_prediction_by_sensor():
    """API ENDPOINT
    The endpoint predicting future temps

    Returns:

    """
    # Loading Database
    db = get_db()

    sensor_name = request.args.get("sensor_name")
    prediction_range = request.args.get("prediction_range")
    
    # Call to Model API

@PUBLIC.route("/processUploadData", methods=["GET", "POST"])
def process_upload_data():
    """API ENDPOINT
    The endpoint predicting future temps

    Returns:

    """
    # Loading Database
    db = get_db()
    sensor_device_service = db.sensor_device_service
    sensor_reading_service = db.sensor_reading_service
    data_dir = "waterTemp_sensorData/" #TODO Add directory for loading data
    COVARIATE_COLUMNS = ['latitude', 'longitude', 'date', 'sea_water_temperature', 'platform']
    for file in os.listdir(data_dir):
        file_dir = os.path.join(data_dir, file)
        csv_data = load_csv_data(file_dir,COVARIATE_COLUMNS)
        sensors = get_unique_sensors(csv_data)
        for sensor in sensors:
            print(sensor)
            sensor_device_obj = sensor_device_service.get_by_name(sensor)
            print(sensor_device_obj)
            if sensor_device_obj is None:
                sensor_device_obj = SensorDevice(str(sensor), "celsius")
                sensor_device_obj = sensor_device_service.add_device(sensor_device_obj)
            sensor_id = sensor_device_obj.id
            #df.loc[df['A'] == 2, 'B'] = 'new_y'
            csv_data.loc[csv_data['platform'] == sensor, 'platform'] = sensor_id
            csv_data.rename(columns={'platform': 'sensor_id', 'sea_water_temperature':'target_reading'}, inplace=True)
            print(csv_data)
            sensor_reading_service.add_rows(csv_data)
        break
    return {'status':200}
=======
    return render_template("homepage/base.html")
>>>>>>> Stashed changes
