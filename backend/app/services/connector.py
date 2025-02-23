import json
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models.connector import Connector
from app.models.connector import ConnectorRequest
from app.repositories.connector import ConnectorRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class ConnectorService(BaseService):
    def __init__(self, db_session: Session):
        """
        Connector service class for handling connector-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._connector_repo = ConnectorRepository(db_session=self._db_session)

    def get_connectors(self) -> Tuple[List[Connector], Optional[APIError]]:
        """
        Get all connectors.

        Returns:
            Tuple[List[Connector], Optional[APIError]]: List of connector objects and APIError object if any error.
        """
        return self._connector_repo.get_connectors()

    def get_connector(self, connector_id: str) -> Tuple[Optional[Connector], Optional[APIError]]:
        """
        Get connector by id.

        Args:
            connector_id(str): Connector id.

        Returns:
            Tuple[Optional[Connector], Optional[APIError]]: Connector object and APIError object if any error.
        """
        return self._connector_repo.get_connector(connector_id=connector_id)

    def create_connector(self, connector_request: ConnectorRequest) -> Optional[APIError]:
        """
        Create new connector.

        Args:
            connector_request(ConnectorRequest): ConnectorRequest object.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        with self._transaction():
            # Define to-be-created connector
            connector = connector_request.model_dump(exclude_unset=True)
            if connector.get("file_paths"):
                connector_specific_config = {"file_paths": connector.get("file_paths")}
                connector["connector_specific_config"] = json.dumps(connector_specific_config)
                connector.pop("file_paths")

            # Create connector
            connector = Connector(**connector)
            err = self._connector_repo.create_connector(connector=connector)

        return err

    def update_connector(
        self, connector_id: str, connector_request: ConnectorRequest
    ) -> Optional[APIError]:
        """
        Update connector by id.

        Args:
            connector_id(str): Connector id.
            connector_request(ConnectorRequest): ConnectorRequest object.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        with self._transaction():
            # Define to-be-updated connector
            connector = connector_request.model_dump(exclude_unset=True)
            if connector.get("file_paths"):
                connector_specific_config = {"file_paths": connector.get("file_paths")}
                connector["connector_specific_config"] = json.dumps(connector_specific_config)
                connector.pop("file_paths")

            # Update connector
            err = self._connector_repo.update_connector(
                connector_id=connector_id, connector=connector
            )

        return err

    def delete_connector(self, connector_id: str) -> Optional[APIError]:
        """
        Delete connector by id.

        Args:
            connector_id(str): Connector id.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        with self._transaction():
            # Delete connector
            err = self._connector_repo.delete_connector(connector_id=connector_id)

        return err
