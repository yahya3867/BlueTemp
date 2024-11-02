"""Database module that contains the DatabaseService Class
used for setting up the database tables and connection"""

# Python Standard Library Imports
import traceback

# Python Third Party Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    Session,
)
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, DatabaseError

# Local Library Imports
from ._create_tables import create_database_tables
from .service import SensorDeviceService, SensorReadingService

class DatabaseService:
    """The service class for setting up the database."""
    def __init__(self, database_url: str, echo: bool = False):
            # Database Connection URL
            self.database_url: str = database_url

            # Whether the database engine is active
            self.active: bool = False

            # Parameter to echo the sql statements or not
            self.echo: bool = echo

            # Creating the database engine
            self.engine: Engine = self._create_db_engine(self.database_url, echo=self.echo)
            self.generate_db_tables()

            if self.active == True:

                # Creating session connection for database
                self.session: Session = self._create_session()

                # Creating the table services.
                self._setup_services()

    def _create_db_engine(self, database_url: str, echo: bool) -> Engine:
        """Creates the database connection engine

        Args:
            database_url (str): The connection url for the database
            echo (bool): A boolean condition to echo the
            sql statements in the console
        Returns:
            Engine: The SQLAlchemy database connection engine
        """
        try:
            return create_engine(
                database_url, pool_recycle=1800, pool_pre_ping=True, echo=echo
            )
        except (SQLAlchemyError, DatabaseError, DBAPIError, RuntimeError) as error:
            print("Error creating database engine")
            traceback.print_tb(error.__traceback__)
            return None
        except Exception as error:
            print("Error:", error)
            traceback.print_tb(error.__traceback__)
            return False

    def generate_db_tables(self):
        """Generates the database tables. If successful sets active to
        true.

        Args:
            engine (Engine): The SQLAlchemy database connection engine
        """
        # If the engine is None then set active to False
        if self.engine is None:
            self.active = False
        # If generating tables was successful set database to active
        if not self.active and create_database_tables(self.engine):
            self.active = True

    def _create_session(self) -> Session:
        """Creates the database shared session object.

        Args:
            engine (Engine): The SQLAlchemy database connection engine

        Returns:
            Session: The shared session object for the
            database services to use.
        """
        # Binding the engine to a session
        self.session_binder = sessionmaker(bind=self.engine)

        # Constructs a scoped session with the session binder
        return scoped_session(self.session_binder)

    def close_session(self):
        """Closes the database connection."""
        self.session: Session
        close_all_sessions()
        self.engine.dispose()

    def _setup_services(self) -> bool:
        try:
            # Setting up the database table services
            self.sensor_device_service = SensorDeviceService(self.session, self.engine)
            self.sensor_reading_service = SensorReadingService(self.session, self.engine)
            return True
        except (SQLAlchemyError, DatabaseError,
                DBAPIError, RuntimeError) as error:
            print("Error creating database services")
            traceback.print_tb(error.__traceback__)
            return False