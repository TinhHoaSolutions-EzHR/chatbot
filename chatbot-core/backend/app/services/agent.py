from io import BytesIO
from typing import List
from typing import Optional
from typing import Tuple

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.databases.minio import MinioConnector
from app.models import Agent
from app.models.agent import AgentRequest
from app.repositories.agent import AgentRepository
from app.services.base import BaseService
from app.settings import Constants
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import construct_file_path
from app.utils.api.helpers import generate_avatar_image
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

        self._agent_repo = AgentRepository(db_session=db_session)
        self._minio_connector = minio_connector

    def get_agents(self, user_id: str) -> Tuple[Optional[List[Agent]], Optional[APIError]]:
        """
        Get all agents of the user. Sort by display_priority.

        Args:
            user_id (str): User id

        Returns:
            Tuple[Optional[List[Agent]], Optional[APIError]]: List of agent objects and APIError object if any error
        """
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
        return self._agent_repo.get_agent(agent_id=agent_id, user_id=user_id)

    def _upload_agent_avatar(
        self,
        agent_avatar: BytesIO,
        agent_name: str,
        user_id: str,
        delete_existing_image: bool = False,
        existing_image_path: str = None,
    ) -> Tuple[str, Optional[APIError]]:
        """
        Upload agent avatar to Minio.

        Args:
            agent_avatar (BytesIO): Agent avatar image
            agent_name (str): Agent name
            user_id (str): User id
            delete_existing_image (bool, optional): Whether to delete existing image. Defaults to False.
            existing_image_path (str, optional): Existing image path. Defaults to None.

        Returns:
            Tuple[str, Optional[APIError]]: File path in Minio and APIError object if any error
        """
        # Construct file path in Minio
        file_path = construct_file_path(object_name=agent_name, user_id=user_id)
        logger.info(f"Uploading agent avatar to Minio: {file_path}")

        # Upload image to Minio
        is_file_uploaded = self._minio_connector.upload_file(
            object_name=file_path,
            data=agent_avatar,
            bucket_name=Constants.MINIO_IMAGE_BUCKET,
        )
        if not is_file_uploaded:
            return "", APIError(kind=ErrorCodesMappingNumber.UNABLE_TO_UPLOAD_FILE_TO_MINIO.value)

        # Delete existing image if needed
        if delete_existing_image and existing_image_path:
            logger.info(f"Deleting existing agent avatar in Minio: {existing_image_path}")
            is_file_deleted = self._minio_connector.delete_file(
                object_name=existing_image_path, bucket_name=Constants.MINIO_IMAGE_BUCKET
            )
            if not is_file_deleted:
                return "", APIError(
                    kind=ErrorCodesMappingNumber.UNABLE_TO_DELETE_FILE_IN_MINIO.value
                )

        return file_path, None

    def create_agent(
        self, agent_request: AgentRequest, user_id: str, file: Optional[UploadFile] = None
    ) -> Optional[APIError]:
        """
        Create a new agent.

        Args:
            agent_request (AgentRequest): Agent request object
            user_id (str): User id
            file (Optional[UploadFile]): File object. Defaults to None.

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Upload image to Minio if file is provided. Otherwise, use the generated image.
            agent_avatar = None
            if not file:
                agent_avatar = generate_avatar_image(data=agent_request.name)
            else:
                agent_avatar = file.file

            # Upload image to Minio
            file_path, err = self._upload_agent_avatar(
                agent_avatar=agent_avatar, agent_name=agent_request.name, user_id=user_id
            )
            if err:
                return err

            # Define agent
            agent = Agent(
                user_id=user_id,
                name=agent_request.name,
                description=agent_request.description,
                agent_type=agent_request.agent_type,
                uploaded_image_path=file_path,
            )

            # Create agent
            err = self._agent_repo.create_agent(agent=agent)

        return err if err else None

    def update_agent(
        self,
        agent_id: str,
        agent_request: AgentRequest,
        user_id: str,
        file: Optional[UploadFile] = None,
    ) -> Optional[APIError]:
        """
        Update an agent.

        Args:
            agent_id (str): Agent id
            agent_request (AgentRequest): Agent request object
            user_id (str): User id
            file (Optional[UploadFile]): File object. Defaults to None.

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define to-be-updated agent
            agent = agent_request.model_dump(exclude_unset=True, exclude_defaults=True)

            # Upload new image to Minio if file is provided.
            if file:
                # Get existing agent
                existing_agent, err = self._agent_repo.get_agent(agent_id=agent_id, user_id=user_id)
                if err:
                    return err

                # Upload image to Minio
                file_path, err = self._upload_agent_avatar(
                    agent_avatar=file.file,
                    agent_name=existing_agent.name,
                    user_id=user_id,
                    delete_existing_image=True,
                    existing_image_path=existing_agent.uploaded_image_path,
                )
                if err:
                    return err

                # Update agent with new image
                agent["uploaded_image_path"] = file_path

            # Update agent
            err = self._agent_repo.update_agent(agent_id=agent_id, agent=agent, user_id=user_id)

        return err if err else None

    def delete_agent(self, agent_id: str, user_id: str) -> Optional[APIError]:
        """
        Delete an agent.

        Args:
            agent_id (str): Agent id
            user_id (str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Get existing agent
            existing_agent, err = self._agent_repo.get_agent(agent_id=agent_id, user_id=user_id)
            if err:
                return err

            if existing_agent.uploaded_image_path:
                # Delete image in Minio
                logger.info(f"Deleting agent avatar in Minio: {existing_agent.uploaded_image_path}")
                is_file_deleted = self._minio_connector.delete_file(
                    object_name=existing_agent.uploaded_image_path,
                    bucket_name=Constants.MINIO_IMAGE_BUCKET,
                )
                if not is_file_deleted:
                    return APIError(
                        kind=ErrorCodesMappingNumber.UNABLE_TO_DELETE_FILE_IN_MINIO.value
                    )

            # Delete agent
            err = self._agent_repo.delete_agent(agent_id=agent_id, user_id=user_id)

        return err if err else None
