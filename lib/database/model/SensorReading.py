"""Module serving as the Model for all the
Sensor Readings"""

# Python Standard Library Imports
from dataclasses import dataclass
from datetime import datetime

# Local Library Imports
from .BaseModel import BaseModel

__all__ = ["SensorReading"]

@dataclass(unsafe_hash=True)
class SensorReading(BaseModel):
    """The dataclass for sensor reading values
    Attributes:
        sensor_id (`int`, `not_nullable`, `foreign_key`):
        The id of the sensor that performed the reading
        target_reading (`float`, `not_nullable`):
        The value of the reading for the sensor
        date (`datetime`, `not_nullable`):
        The time the reading was taken.
        qcflag(`int`, `nullable`):
        The flag for qc unknown what this does.
        network (`varchar`, `nullable`):
        The network where the sensor reading took place.
        longitude (`float`, `not_nullable`):
        The longitudal location of the sensor
        at time of reading
        latitude (`float`, `not_nullable`):
        The latitudal location of the sensor
        at time of reading"""

    # Type Hinting all class attributes
    # for this database table
    id : int
    date : datetime
    latitude: float
    longitude: float
    target_reading: float
    sensor_id: int

    # Initializing the attributes in
    # the pythonic class
    def __init__(self,
                 date,
                 latitude,
                 longitude,
                 target_reading,
                 sensor_id):
        self.date = date
        self.latitude = latitude
        self.longitude = longitude
        self.target_reading = target_reading
        self.sensor_id = sensor_id

