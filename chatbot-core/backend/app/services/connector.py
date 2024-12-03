import json
from typing import List
from typing import Tuple
from typing import Union

from sqlalchemy.orm import Session

from app.models.api import APIError
from app.models.connector import Connector
from app.models.connector import ConnectorRequest
from app.models.connector import DocumentSource
from app.repositories.connector import ConnectorRepository
from app.services.base import BaseService
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class ConnectorService(BaseService):
    def __init__(self, db_session: Session):
        """
        Connector service class for handling connector-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_connectors(self) -> Tuple[List[Connector], APIError | None]:
        """
        Get all connectors

        Returns:
            Tuple[List[Connector], Union[APIError, None]]: List of connector objects and APIError object if any error
        """
        return ConnectorRepository(db_session=self._db_session).get_connectors()

    def get_connector(self, connector_id: str) -> Tuple[Connector, Union[APIError, None]]:
        """
        Get connector by connector_id

        Args:
            connector_id(str): Connector id

        Returns:
            Tuple[Connector, Union[APIError, None]]: Connector object and APIError object if any error
        """
        return ConnectorRepository(db_session=self._db_session).get_connector(connector_id=connector_id)

    def create_connector(self, connector_request: ConnectorRequest) -> Union[APIError, None]:
        """
        Create connector

        Args:
            connector_request(ConnectorRequest): ConnectorRequest object

        Returns:
            Union[APIError, None]: APIError object if any error
        """
        err = None
        try:
            with self._transaction():
                # Define connector
                connector_specific_config = {"file_paths": [file_path for file_path in connector_request.file_paths]}
                connector = Connector(
                    name=connector_request.name,
                    source=DocumentSource.FILE,
                    connector_specific_config=json.dumps(connector_specific_config),
                )

                # Create connector
                err = ConnectorRepository(db_session=self._db_session).create_connector(connector=connector)
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error creating connector: {e}", exc_info=True)
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    def update_connector(self, connector_id: str, connector_request: ConnectorRequest) -> Union[APIError, None]:
        """
        Update connector by connector_id

        Args:
            connector_id(str): Connector id
            connector_request(ConnectorRequest): ConnectorRequest object

        Returns:
            Union[APIError, None]: APIError object if any error
        """
        err = None
        try:
            with self._transaction():
                # Define connector
                connector = Connector(name=connector_request.name)

                err = ConnectorRepository(db_session=self._db_session).update_connector(
                    connector_id=connector_id, connector=connector
                )
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error updating connector: {e}", exc_info=True)
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    def delete_connector(self, connector_id: str) -> Union[APIError, None]:
        """
        Delete connector by connector_id

        Args:
            connector_id(str): Connector id

        Returns:
            Union[APIError, None]: APIError object if any error
        """
        try:
            with self._transaction():
                # Delete connector
                err = ConnectorRepository(db_session=self._db_session).delete_connector(connector_id=connector_id)
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error deleting connector: {e}", exc_info=True)
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err
