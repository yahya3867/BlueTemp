"""Database module for defining the SensorDeviceRepository Class"""

# Python Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..model import SensorDevice
from .BaseRepository import BaseRepository

__all__ = ["SensorDeviceRepository"]


class SensorDeviceRepository(BaseRepository):
    """The class for interacting/querying the `sensor_devices` sql table.
    Args:
        session(sqlalchemy.orm.Session): The database session object
        to use for querying and commiting changes.
    """

    def __init__(self, session: Session, engine):
        # Initializes the base repository class
        super().__init__(session=session, model=SensorDevice, table_name="sensor_devices", engine=engine)