"""Database module for defining the BaseRepository Class"""

# Python Standard Library Imports
import traceback
from typing import Any, List, Optional

# Python Third Party Imports
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, DatabaseError
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

__all__ = ["BaseRepository"]


class BaseRepository:
    """The base class for interacting/querying a SQL table.

    Args:
        session (Session): The database session object to use for querying and committing changes.
        table_name (str): The name of the table in the SQL Database.
        model (Any): The Python model class for the database.
    """

    def __init__(self, session: Session, table_name: str, model, engine):
        self.session: Session = session
        self.table_name: str = table_name
        self.model = model
        self.attributes = self.model.__annotations__.keys()
        self.engine = engine

    def commit_changes(self) -> bool:
        """Utility function to commit changes to the database."""
        try:
            self.session.commit()
            return True
        except (SQLAlchemyError, DatabaseError, DBAPIError, RuntimeError) as error:
            print(f"Error committing changes to the {self.table_name} table")
            print(error)
            traceback.print_tb(error.__traceback__)
            self.session.rollback()
            return False

    def add_row(self, database_obj: Any) -> Optional[Any]:
        """Adds a new row to the database table.

        Args:
            database_obj (Any): The database object to add to the database.

        Returns:
            Optional[Any]: Returns the database object added
                to its respective table, or None if the commit failed.
        """
        self.session.add(database_obj)
        if not self.commit_changes():
            return None
        return database_obj

    def get_by_id(self, object_id: int) -> Optional[Any]:
        """Gets a database object by its ID.

        Args:
            object_id (int): The ID associated with a table row.

        Returns:
            Optional[Any]: The database row represented as a Python model, or None if not found.
        """
        if "id" not in self.attributes:
            raise SQLAlchemyError(
                f"Error: The table {self.table_name} does not have an 'id' column"
            )

        stmt = select(self.model).where(self.model.id == object_id)
        try:
            result = self.session.scalars(stmt).first()
            return result
        except SQLAlchemyError as e:
            print(f"Error fetching by id {object_id} from {self.table_name}")
            print(e)
            return None

    def delete_row_by_id(self, object_id: int) -> bool:
        """Deletes a row by its ID from the database.

        Args:
            object_id (int): The ID associated with a table row.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        if "id" not in self.attributes:
            raise SQLAlchemyError(
                f"Error: The table {self.table_name} does not have an 'id' column"
            )

        stmt = delete(self.model).where(self.model.id == object_id)
        try:
            self.session.execute(stmt)
            return self.commit_changes()
        except SQLAlchemyError as e:
            print(f"Error deleting id {object_id} from {self.table_name}")
            print(e)
            self.session.rollback()
            return False

    def get_by_ids(self, object_id_list: List[int]) -> List[Any]:
        """Gets a list of rows by a list of IDs from the database.

        Args:
            object_id_list (List[int]): The list of row ids to retrieve.

        Returns:
            List[Any]: The list of database objects, empty if none found.
        """
        if "id" not in self.attributes:
            raise SQLAlchemyError(
                f"Error: The table {self.table_name} does not have an 'id' column"
            )

        stmt = select(self.model).where(self.model.id.in_(object_id_list))
        try:
            results = self.session.scalars(stmt).all()
            return results
        except SQLAlchemyError as e:
            print(f"Error fetching by ids from {self.table_name}")
            print(e)
            return []

    def get_first_by_args(self, **kwargs) -> Optional[Any]:
        """Gets the first database object matching the provided keyword arguments.

        Args:
            **kwargs (Any): Keyword arguments matching the column names.

        Returns:
            Optional[Any]: The database object or None if not found.
        """
        stmt = select(self.model).filter_by(**kwargs)
        try:
            result = self.session.scalars(stmt).first()
            return result
        except Exception as e:
            print(f"Error fetching with args {kwargs} from {self.table_name}")
            print(e)
            return None

    def get_all_by_args(self, **kwargs) -> List[Any]:
        """Gets all database objects matching the provided keyword arguments.

        Args:
            **kwargs (Any): Keyword arguments matching the column names.

        Returns:
            List[Any]: The list of database objects, empty if none found.
        """
        stmt = select(self.model).filter_by(**kwargs)
        try:
            results = self.session.scalars(stmt).all()
            return results
        except SQLAlchemyError as e:
            print(f"Error fetching with args {kwargs} from {self.table_name}")
            print(e)
            return []