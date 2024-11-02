"""Database module for SensorReadingService class that interacts
with the `sensor_readings` table"""

# Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..repository import SensorReadingRepository
from .BaseService import BaseService
from ..model import SensorReading

__all__ = ["SensorReadingService"]

class SensorReadingService(BaseService):
    """The Sensor Reading Service class for interacting with
    the repository classes.
    """
    def __init__(self, session: Session, engine):
        # Initializing the repository and distributing the
        # database session
        super().__init__(session, SensorReadingRepository, engine)
        self.repo: SensorReadingRepository

    def add_row(self, sensor_reading_obj: SensorReading) -> SensorReading:
        """Service function for adding a sensor reading entry to the
        database

        Args:
            sensor_reading_obj (SensorReading): The sensor reading orm class to add.

        Returns:
            SensorReading: The newly added SensorReading. Will be None if it
            fails.
        """

        # Adding the sensor reading to database
        return self.add(sensor_reading_obj)
    
    def add_rows(self, dataframe):
        """Service function for adding a sensor reading entry to the
        database

        Args:
            sensor_reading_obj (SensorReading): The sensor reading orm class to add.

        Returns:
            SensorReading: The newly added SensorReading. Will be None if it
            fails.
        """

        # Adding the sensor reading to database
        return self.repo.add_dataframe_bulk(dataframe)