from io import BytesIO
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.databases.minio import MinioConnector
from app.models import Agent
from app.models import StarterMessage
from app.models.agent import AgentRequest
from app.repositories.agent import AgentRepository
from app.services.base import BaseService
from app.settings import Constants
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.file import construct_file_path
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class AgentService(BaseService):
    def __init__(self, db_session: Session, minio_connector: Optional[MinioConnector] = None):
        """
        Agent service class for handling agent-related operations.

        Args:
            db_session (Session): Database session
            minio_connector (MinioConnector, optional): Object storage connection. Defaults to None.
        """
        super().__init__(db_session)

        # Define repositories
        self._agent_repo = AgentRepository(db_session=db_session)

    def get_agents(self, user_id: str) -> Tuple[Optional[List[Agent]], Optional[APIError]]:
        """
        Get all agents of the user.

        Args:
            user_id (str): User id

        Returns:
            Tuple[Optional[List[Agent]], Optional[APIError]]: List of agent objects and APIError object if any error
        """
        # Get agents
        return self._agent_repo.get_agents(user_id=user_id)

    def get_agent(self, agent_id: str, user_id: str) -> Tuple[Optional[Agent], Optional[APIError]]:
        """
        Get an agent by id.

        Args:
            agent_id (str): Agent id
            user_id (str): User id

        Returns:
            Tuple[Optional[Agent], Optional[APIError]]: Agent object and APIError object if any error
        """
        # Get agent by id
        return self._agent_repo.get_agent(agent_id=agent_id, user_id=user_id)

    def _upload_agent_avatar(
        self,
        agent_avatar: BytesIO,
        agent_name: str,
        user_id: str,
        delete_existing_image: bool = False,
        existing_image_path: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[APIError]]:
        """
        Upload agent avatar to Minio.

        Args:
            agent_avatar (BytesIO): Agent avatar image.
            agent_name (str): Agent name.
            user_id (str): User id.
            delete_existing_image (bool): Delete existing image. Defaults to False.
            existing_image_path (Optional[str]): Existing image path. Defaults to None.

        Returns:
            Tuple[Optional[str], Optional[APIError]]: File path in Minio and APIError object if any error
        """
        # Delete existing image if needed
        if delete_existing_image and existing_image_path:
            logger.info(f"Deleting existing agent avatar in Minio: {existing_image_path}")
            is_file_deleted = self._minio_connector.delete_file(
                object_name=existing_image_path, bucket_name=Constants.MINIO_IMAGE_BUCKET
            )
            if not is_file_deleted:
                return None, APIError(
                    kind=ErrorCodesMappingNumber.UNABLE_TO_DELETE_FILE_FROM_MINIO.value
                )

        # Construct file path in Minio
        file_path = construct_file_path(object_name=agent_name, user_id=str(user_id))
        logger.info(f"Uploading agent avatar to Minio: {file_path}")

        # Upload image to Minio
        is_file_uploaded = self._minio_connector.upload_file(
            object_name=file_path,
            data=agent_avatar,
            bucket_name=Constants.MINIO_IMAGE_BUCKET,
        )
        if not is_file_uploaded:
            return None, APIError(kind=ErrorCodesMappingNumber.UNABLE_TO_UPLOAD_FILE_TO_MINIO.value)

        return file_path, None

    def create_agent(
        self,
        agent_request: AgentRequest,
        user_id: str,
    ) -> Optional[APIError]:
        """
        Create a new agent.

        Args:
            agent_request (AgentRequest): Agent request object.
            user_id (str): User id.
            file (Optional[UploadFile]): File object. Defaults to None.

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define agent and create it
            agent = Agent(
                user_id=user_id,
                **agent_request.model_dump(exclude={"starter_messages"}),
            )
            err = self._agent_repo.create_agent(agent=agent)
            if err:
                return err

            # Flush to get the agent id
            self._db_session.flush()

            # Get the created agent id
            agent_id = agent.id

            # Define starter messages and create them
            for starter_messages_request in agent_request.starter_messages:
                starter_message = StarterMessage(
                    agent_id=agent_id, **starter_messages_request.model_dump()
                )
                err = self._agent_repo.create_starter_message(starter_message=starter_message)
                if err:
                    return err

        return None

    def update_agent(
        self,
        agent_id: str,
        agent_request: AgentRequest,
        user_id: str,
    ) -> Optional[APIError]:
        """
        Update an agent.

        Args:
            agent_id (str): Agent id.
            agent_request (AgentRequest): Agent request object.
            user_id (str): User id.
            file (Optional[UploadFile]): File object. Defaults to None.

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define to-be-updated agent
            agent = agent_request.model_dump(exclude_unset=True, exclude={"starter_messages"})
            logger.info(f"Updating agent: {agent}")

            # Update agent
            err = self._agent_repo.update_agent(agent_id=agent_id, agent=agent, user_id=user_id)
            if err:
                return err

            # Update starter messages if provided
            if agent_request.starter_messages:
                for starter_message_request in agent_request.starter_messages:
                    # Define to-be-updated starter message
                    starter_message = starter_message_request.model_dump(exclude_unset=True)

                    # Update starter message
                    err = self._agent_repo.update_starter_message(
                        starter_message_id=starter_message_request.id,
                        agent_id=agent_id,
                        starter_message=starter_message,
                    )
                    if err:
                        return err

        return None

    def delete_agent(self, agent_id: str, user_id: str) -> Optional[APIError]:
        """
        Delete an agent.
        1. Delete the starter messages assiciaed with the agent.
        2. Delete the agent.
        3. Clean up the image in Minio.

        Args:
            agent_id (str): Agent id.
            user_id (str): User id.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        with self._transaction():
            # Get existing agent
            existing_agent, err = self._agent_repo.get_agent(agent_id=agent_id, user_id=user_id)
            if err:
                return err

            # Delete the agent
            err = self._agent_repo.delete_agent(agent_id=agent_id, user_id=user_id)
            if err:
                return err

            # Delete the image uploaded in MinIO
            if existing_agent.uploaded_image_path:
                logger.info(f"Deleting agent avatar in Minio: {existing_agent.uploaded_image_path}")
                is_file_deleted = self._minio_connector.delete_file(
                    object_name=existing_agent.uploaded_image_path,
                    bucket_name=Constants.MINIO_IMAGE_BUCKET,
                )
                if not is_file_deleted:
                    return APIError(
                        kind=ErrorCodesMappingNumber.UNABLE_TO_DELETE_FILE_IN_MINIO.value
                    )

        return None
