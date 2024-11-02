"""Database module for SensorDeviceService class that interacts
with the `sensor_devices` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import SensorDeviceRepository
from .BaseService import BaseService
from ..model import SensorDevice

__all__ = ["SensorDeviceService"]

class SensorDeviceService(BaseService):
    """The Sensor Device Service class for interacting with
    the repository classes.
    """

    def __init__(self, session: Session, engine):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, SensorDeviceRepository, engine)
        self.repo: SensorDeviceRepository

    def add_device(self, sensor_device_obj: SensorDevice) -> SensorDevice:
        """Service function for adding a sensor device entry to the
        database

        Args:
            sensor_device_obj (SensorDevice): The sensor device orm class to add.

        Returns:
            SensorDevice: The newly added SensorDevice. Will be None if it
            fails.
        """

        # Adding the sensor device to database
        return self.add(sensor_device_obj)
    
    def get_by_name(self, sensor_device_name:str) -> SensorDevice:
        """Service function for retrieving a sensor device row by matching the name.

        Args:
            sensor_device_name (str): The name of the sensor device

        Returns:
            SensorDevice: The database model object for SensorDevice.
        """

        # Getting the SensorDevice object
        return self.repo.get_first_by_args(name=sensor_device_name)