"""Module for storing the database model classes"""
# Location
# lib\database\model\__init__.py

# Files
from .BaseModel import BaseModel
from .SensorDevice import SensorDevice
from .SensorReading import SensorReading


__all__ = ["SensorDevice","SensorReading"]