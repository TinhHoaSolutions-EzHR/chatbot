from typing import List
from typing import Tuple
from typing import Union
from sqlalchemy.orm import Session

from app.models.api import APIError
from app.models.connector import Connector
from app.repositories.base import BaseRepository
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class ConnectorRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Connector repository class for handling connector-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_connectors(self) -> Tuple[List[Connector], Union[APIError, None]]:
        """
        Get all connectors

        Returns:
            Tuple[List[Connector], Union[APIError, None]]: List of connector objects and APIError object if any error
        """
        try:
            connectors = self._db_session.query(Connector).all()
            return connectors, None
        except Exception as e:
            logger.error(f"Error getting connectors: {e}", exc_info=True)
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_connector(self, connector_id: str) -> Tuple[Connector, Union[APIError, None]]:
        """
        Get connector by connector_id

        Args:
            connector_id(str): Connector id

        Returns:
            Tuple[Connector, Union[APIError, None]]: Connector object and APIError object if any error
        """
        try:
            connector = self._db_session.query(Connector).filter(Connector.id == connector_id).first()
            return connector, None
        except Exception as e:
            logger.error(f"Error getting connector: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_connector(self, connector: Connector) -> Union[APIError, None]:
        """
        Create connector

        Args:
            connector(Connector): Connector object

        Returns:
            Union[APIError, None]: APIError object if any error
        """
        try:
            self._db_session.add(connector)
            return None
        except Exception as e:
            logger.error(f"Error creating connector: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_connector(self, connector_id: str, connector: Connector) -> Union[APIError, None]:
        """
        Update connector by connector_id

        Args:
            connector_id(str): Connector id
            connector(Connector): Connector object

        Returns:
            Union[APIError, None]: APIError object if any error
        """
        try:
            connector = {key: value for key, value in connector.__dict__.items() if not key.startswith("_")}
            self._db_session.query(Connector).filter(Connector.id == connector_id).update(connector)
            return None
        except Exception as e:
            logger.error(f"Error updating connector: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_connector(self, connector_id: str) -> Union[APIError, None]:
        """
        Delete connector by connector_id

        Args:
            connector_id(str): Connector id

        Returns:
            Union[APIError, None]: APIError object if any error
        """
        try:
            self._db_session.query(Connector).filter(Connector.id == connector_id).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting connector: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
