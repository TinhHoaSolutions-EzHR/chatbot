from sqlalchemy.orm import Session
from typing import List, Tuple

from app.models.api import APIError
from app.models.connector import Connector
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class ConnectorRepository:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get_connectors(self) -> Tuple[List[Connector], APIError | None]:
        """
        Get all connectors

        Returns:
            Tuple[List[Connector], APIError | None]: List of connector objects and APIError object if any error
        """
        try:
            connectors = self._db_session.query(Connector).all()
            return connectors, None
        except Exception as e:
            logger.error(f"Error getting connectors: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_connector(self, connector_id: int) -> Tuple[Connector, APIError | None]:
        """
        Get connector by connector_id

        Args:
            connector_id(int): Connector id

        Returns:
            Tuple[Connector, APIError | None]: Connector object and APIError object if any error
        """
        try:
            connector = self._db_session.query(Connector).filter(Connector.id == connector_id).first()
            if not connector:
                return None, APIError(kind=ErrorCodesMappingNumber.NOT_FOUND.value)
            return connector, None
        except Exception as e:
            logger.error(f"Error getting connector: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_connector(self, connector: Connector) -> APIError | None:
        """
        Create connector

        Args:
            connector(Connector): Connector object

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            self._db_session.add(connector)
            self._db_session.commit()
            return None
        except Exception as e:
            logger.error(f"Error creating connector: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_connector(self, connector_id: int, connector: Connector) -> APIError | None:
        """
        Update connector by connector_id

        Args:
            connector_id(int): Connector id
            connector(Connector): Connector object

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            connector = {key: value for key, value in connector.__dict__.items() if not key.startswith("_")}
            self._db_session.query(Connector).filter(Connector.id == connector_id).update(connector)
            self._db_session.commit()
            return None
        except Exception as e:
            logger.error(f"Error updating connector: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_connector(self, connector_id: int) -> APIError | None:
        """
        Delete connector by connector_id

        Args:
            connector_id(int): Connector id

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            self._db_session.query(Connector).filter(Connector.id == connector_id).delete()
            self._db_session.commit()
            return None
        except Exception as e:
            logger.error(f"Error deleting connector: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
