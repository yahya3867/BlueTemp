"""The blueprint API route for all public endpoints"""
# Python Standard Library Imports
from datetime import datetime
import os

# Python Third Party Imports
from flask import Blueprint, render_template, request, jsonify

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
    return render_template("index.html")

@PUBLIC.route("/demo", methods=["GET", "POST"])
def demo():
    """API ENDPOINT
    The endpoint for rendering the demo page

    Returns:
        render_template: Renders the tool
        html
    """
    return render_template("tool.html")


@PUBLIC.route("/getPredictionBySensor", methods=["GET", "POST"])
def get_prediction_by_sensor():
    """API ENDPOINT
    The endpoint predicting future temps

    Returns:

    """
    # Loading Database
    db = get_db()

    sensor_device_service = db.sensor_device_service
    sensor_reading_service = db.sensor_reading_service
    # Name of Sensor
    sensor_name = request.args.get("sensor_name", default=None)

    # Start and End Dates
    prediction_range_low = request.args.get("prediction_range_low")
    prediction_range_high = request.args.get("prediction_range_high")

    # "2010-01-01 1:01:01" example date range format
    sensor_device_obj = sensor_device_service.get_by_name(sensor_name)
    start_date = datetime.strptime(prediction_range_low, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(prediction_range_high, "%Y-%m-%d %H:%M:%S")
    df = sensor_reading_service.get_by_date_sensor(start_date, end_date, sensor_id=sensor_device_obj.id)
    return {'status':200}
    # Call to Model API

@PUBLIC.route("/getAllSensors", methods=["GET", "POST"])
def get_all_sensors():
    db = get_db()
    sensor_device_service = db.sensor_device_service
    sensor_device_obj_list = sensor_device_service.get_all_sensors()
    return jsonify(sensor_device_obj_list)

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
    #data_dir = request.args.get("data_dir", default=None, type=str) #TODO Add directory for loading data
    data_dir = "data"
    COVARIATE_COLUMNS = ['latitude', 'longitude', 'date', 'sea_water_temperature', 'platform']
    for file in os.listdir(data_dir):
        try:
            file_dir = os.path.join(data_dir, file)
            csv_data = load_csv_data(file_dir,COVARIATE_COLUMNS)
            sensors = get_unique_sensors(csv_data)
            for sensor in sensors:
                sensor_device_obj = sensor_device_service.get_by_name(sensor)
                if sensor_device_obj is None:
                    sensor_device_obj = SensorDevice(str(sensor),
                                                     "celsius",
                                                     csv_data.where(csv_data['platform'] == sensor).head(1)['latitude'][0],
                                                     csv_data.where(csv_data['platform'] == sensor).head(1)['longitude'][0])
                    sensor_device_obj = sensor_device_service.add_device(sensor_device_obj)
                sensor_id = sensor_device_obj.id
                csv_data.loc[csv_data['platform'] == sensor, 'platform'] = sensor_id
                csv_data.rename(columns={'platform': 'sensor_id', 'sea_water_temperature':'target_reading'}, inplace=True)
                sensor_reading_service.add_rows(csv_data)
        except:
            break
            continue
    return {'status':200}
