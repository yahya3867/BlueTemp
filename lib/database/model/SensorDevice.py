"""Module serving as the Model for all the
Sensors"""

# Python Standard Library Imports
from dataclasses import dataclass

# Local Library Imports
from .BaseModel import BaseModel

__all__ = ["SensorDevice"]

@dataclass(unsafe_hash=True)
class SensorDevice(BaseModel):
    """The base dataclass for the database tables.
    The id assigned to a sensor reading
    Attributes:
        id (`int`, `primary-key`, `auto-increment`):
        The id associated with the sensor.
        name (`varchar`, `not_nullable`):
        Name of the sensor, stored as a string.
        target_reading_type (`varchar`, `not_nullable`):
        A string value to identify the target datatype
        of the sensor
    """
    # Type Hinting all class attributes
    # for this database table
    id: int
    name : str
    target_reading_type: str

    # Initializing the attributes in
    # the pythonic class
    def __init__(self,
                 id,
                 name,
                 target_reading_type):
        self.id = id
        self.name = name
        self.target_reading_type = target_reading_type

