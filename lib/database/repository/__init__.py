"""Module for storing the database repository classes,
the repository classes handle direct queries to the database"""
# Location
# lib\database\repository\__init__.py

# Files
from .SensorDeviceRepository import SensorDeviceRepository
from .SensorReadingRepository import SensorReadingRepository

__all__ = ["SensorDeviceRepository","SensorReadingRepository"]