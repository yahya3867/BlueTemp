"""Database module for defining the SensorReadingRepository Class"""

# Python Third Party Imports
from sqlalchemy.orm import Session

# Local Library Imports
from ..model import SensorReading
from .BaseRepository import BaseRepository

__all__ = ["SensorReadingRepository"]


class SensorReadingRepository(BaseRepository):
    """The class for interacting/querying the `sensor_readings` sql table.
    Args:
        session(sqlalchemy.orm.Session): The database session object
        to use for querying and commiting changes.
    """

    def __init__(self, session: Session, engine):
        # Initializes the base repository class
        super().__init__(session=session, model=SensorReading, table_name="sensor_readings", engine=engine)

    def add_dataframe_bulk(self, dataframe):
        print("TEST")
        dataframe.to_sql('sensor_readings', self.engine, if_exists='append', index=False)
        print("TEST2")
        return True