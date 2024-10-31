"""Module for generating the database tables"""

# Python Standard Library Imports
import traceback


# Python Third Party Imports
from sqlalchemy.orm import relationship
from sqlalchemy.orm import registry
from sqlalchemy.engine import Engine
from sqlalchemy import (Table, Column,
                        Integer, ForeignKey,
                        MetaData, DateTime,
                        String, Float)
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, DatabaseError

# Local Library Imports
from .model import SensorDevice, SensorReading

__all__ = ["create_database_tables"]

def create_database_tables(engine: Engine) -> bool:
    """Maps out and generates all the tables for
    the database

    Args:
        engine (Engine): The SQL engine object to use
        for connecting and manipulating the database.

    Returns:
        bool: Returns true if the tables are successfully made.
        Otherwise returns False if there are errors.
    """
    try:
        # Registry for mapping the tables
        mapper_registry = registry()

        # Metadata object to share between tables
        metadata = mapper_registry.metadata

        # Creating the map for the sensor devices table
        sensor_device_table = Table("sensor_devices",
                                    metadata,
                                    Column("id", Integer, primary_key=True, autoincrement=True),
                                    Column("name", String(50), nullable=False, unique=True),
                                    Column("target_reading_type", String(50), nullable=False,)
                                    )

        # Creating the map for the sensor reading values
        sensor_reading_table = Table("sensor_readings",
                                    metadata,
                                    Column("sensor_id", Integer, nullable=False),
                                    Column("target_reading", Float, nullable=False),
                                    Column("date", DateTime, nullable=False),
                                    Column("qcflag", Integer),
                                    Column("network", String(50)),
                                    Column("longitude", Float, nullable=False),
                                    Column("latitude", Float, nullable=False),
                                    )

        # Mapping the relationships of the SensorDevice table
        # Sets the foreign key for sensor readings table
        registry.map_imperatively(SensorDevice,
                                sensor_device_table,
                                properties={
                                    "sensor_readings": relationship(SensorReading,
                                                                    primaryjoin=sensor_device_table.c.id == sensor_reading_table.c.sensor_id)
                                }
        )
        # Mapping the relationships of the Sensor Reading table
        registry.map_imperatively(SensorReading,sensor_reading_table)

        # Creating the tables after mapping out columns and relationships
        mapper_registry.metadata.create_all(engine)

        return True
    except (SQLAlchemyError, DBAPIError,
            DatabaseError) as error:
        print("Error generating database tables")
        traceback.print_tb(error.__traceback__)
        return False





