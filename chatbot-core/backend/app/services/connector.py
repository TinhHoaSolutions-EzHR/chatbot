from sqlalchemy.orm import Session
from typing import List, Tuple

from app.models.api import APIError
from app.models.connector import Connector, ConnectorRequest, DocumentSource
from app.repositories.connector import ConnectorRepository
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class ConnectorService:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get_connectors(self) -> Tuple[List[Connector], APIError | None]:
        """
        Get all connectors

        Returns:
            Tuple[List[Connector], APIError | None]: List of connector objects and APIError object if any error
        """
        return ConnectorRepository(db_session=self._db_session).get_connectors()

    def get_connector(self, connector_id: int) -> Tuple[Connector, APIError | None]:
        """
        Get connector by connector_id

        Args:
            connector_id(int): Connector id

        Returns:
            Tuple[Connector, APIError | None]: Connector object and APIError object if any error
        """
        return ConnectorRepository(db_session=self._db_session).get_connector(connector_id=connector_id)

    def create_connector(self, connector_request: ConnectorRequest) -> APIError | None:
        """
        Create connector

        Args:
            connector_request(ConnectorRequest): ConnectorRequest object

        Returns:
            APIError | None: APIError object if any error
        """
        err = None
        try:
            # Begin transaction
            self._db_session.begin()

            # Define connector
            connector_specific_config = {"file_paths": [file_path for file_path in connector_request.file_paths]}
            connector = Connector(
                name=connector_request.name,
                source=DocumentSource.FILE,
                connector_specific_config=connector_specific_config,
            )

            # Create connector
            err = ConnectorRepository(db_session=self._db_session).create_connector(connector=connector)

            # Commit transaction
            self._db_session.commit()
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error creating connector: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    def update_connector(self, connector_id: int, connector_request: ConnectorRequest) -> APIError | None:
        """
        Update connector by connector_id

        Args:
            connector_id(int): Connector id
            connector_request(ConnectorRequest): ConnectorRequest object

        Returns:
            APIError | None: APIError object if any error
        """
        err = None
        try:
            # Begin transaction
            self._db_session.begin()

            # Define connector
            connector = Connector(name=connector_request.name)

            err = ConnectorRepository(db_session=self._db_session).update_connector(
                connector_id=connector_id, connector=connector
            )

            # Commit transaction
            self._db_session.commit()
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error updating connector: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    def delete_connector(self, connector_id: int) -> APIError | None:
        """
        Delete connector by connector_id

        Args:
            connector_id(int): Connector id

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            # Begin transaction
            self._db_session.begin()

            err = ConnectorRepository(db_session=self._db_session).delete_connector(connector_id=connector_id)

            # Commit transaction
            self._db_session.commit()
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error deleting connector: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err
