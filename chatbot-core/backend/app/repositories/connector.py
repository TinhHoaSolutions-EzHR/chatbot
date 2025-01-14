from typing import Any
from typing import Dict
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
            db_session (Session): Database session.
        """
        super().__init__(db_session=db_session)

    def get_connectors(self) -> Tuple[List[Connector], Optional[APIError]]:
        """
        Get all connectors.

        Returns:
            Tuple[List[Connector], Optional[APIError]]: List of connector objects and APIError object if any error.
        """
        try:
            # Get connectors
            connectors = self._db_session.query(Connector).all()
            return connectors, None
        except Exception as e:
            logger.error(f"Error getting connectors: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_connector(self, connector_id: str) -> Tuple[Optional[Connector], Optional[APIError]]:
        """
        Get connector by connector_id.

        Args:
            connector_id(str): Connector id.

        Returns:
            Tuple[Optional[Connector], Optional[APIError]]: Connector object and APIError object if any error.
        """
        try:
            # Get connector
            connector = (
                self._db_session.query(Connector).filter(Connector.id == connector_id).first()
            )
            if not connector:
                return None, APIError(kind=ErrorCodesMappingNumber.CONNECTOR_NOT_FOUND.value)

            return connector, None
        except Exception as e:
            logger.error(f"Error getting connector: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_connector(self, connector: Connector) -> Optional[APIError]:
        """
        Create connector.

        Args:
            connector(Connector): Connector object.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        try:
            # Create connector
            self._db_session.add(connector)
            return None
        except Exception as e:
            logger.error(f"Error creating connector: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_connector(self, connector_id: str, connector: Dict[str, Any]) -> Optional[APIError]:
        """
        Update connector by connector_id.

        Args:
            connector_id(str): Connector id.
            connector(Dict[str, Any]): Connector object.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        try:
            # Check if connector exists
            connector_exists = (
                self._db_session.query(Connector).filter(Connector.id == connector_id).first()
            )
            if not connector_exists:
                return APIError(kind=ErrorCodesMappingNumber.CONNECTOR_NOT_FOUND.value)

            # Update connector
            self._db_session.query(Connector).filter(Connector.id == connector_id).update(connector)
            return None
        except Exception as e:
            logger.error(f"Error updating connector: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_connector(self, connector_id: str) -> Optional[APIError]:
        """
        Delete connector by connector_id.

        Args:
            connector_id(str): Connector id.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        try:
            # Check if connector exists
            connector_exists = (
                self._db_session.query(Connector).filter(Connector.id == connector_id).first()
            )
            if not connector_exists:
                return APIError(kind=ErrorCodesMappingNumber.CONNECTOR_NOT_FOUND.value)

            # Delete connector
            self._db_session.query(Connector).filter(Connector.id == connector_id).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting connector: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
