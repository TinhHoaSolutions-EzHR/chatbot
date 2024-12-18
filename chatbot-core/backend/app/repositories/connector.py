from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models.connector import Connector
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class ConnectorRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Connector repository class for handling connector-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_connectors(self) -> Tuple[List[Connector], Optional[APIError]]:
        """
        Get all connectors

        Returns:
            Tuple[List[Connector], Optional[APIError]]: List of connector objects and APIError object if any error
        """
        try:
            connectors = self._db_session.query(Connector).all()
            return connectors, None
        except Exception as e:
            logger.error(f"Error getting connectors: {e}", exc_info=True)
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_connector(self, connector_id: str) -> Tuple[Connector, Optional[APIError]]:
        """
        Get connector by connector_id

        Args:
            connector_id(str): Connector id

        Returns:
            Tuple[Connector, Optional[APIError]]: Connector object and APIError object if any error
        """
        try:
            connector = (
                self._db_session.query(Connector).filter(Connector.id == connector_id).first()
            )
            return connector, None
        except Exception as e:
            logger.error(f"Error getting connector: {e}", exc_info=True)
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_connector(self, connector: Connector) -> Optional[APIError]:
        """
        Create connector

        Args:
            connector(Connector): Connector object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(connector)
            return None
        except Exception as e:
            logger.error(f"Error creating connector: {e}", exc_info=True)
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_connector(self, connector_id: str, connector: Connector) -> Optional[APIError]:
        """
        Update connector by connector_id

        Args:
            connector_id(str): Connector id
            connector(Connector): Connector object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            connector = {
                key: value for key, value in connector.__dict__.items() if not key.startswith("_")
            }
            self._db_session.query(Connector).filter(Connector.id == connector_id).update(connector)
            return None
        except Exception as e:
            logger.error(f"Error updating connector: {e}", exc_info=True)
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_connector(self, connector_id: str) -> Optional[APIError]:
        """
        Delete connector by connector_id

        Args:
            connector_id(str): Connector id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(Connector).filter(Connector.id == connector_id).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting connector: {e}", exc_info=True)
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
