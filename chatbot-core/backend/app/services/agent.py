import hashlib
import os
from datetime import datetime
from io import BytesIO
from typing import List
from typing import Optional
from typing import Tuple

import pydenticon
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
from app.utils.api.helpers import get_logger
from app.utils.api.helpers import remove_vietnamese_accents

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
            # Construct file path in Minio
            file_name = (
                (remove_vietnamese_accents(input_str=agent_request.name).replace(" ", "_").lower())
                + "_"
                + user_id
                + datetime.now().strftime("%Y%m%d%H%M%S")
                + ".png"
            )
            logger.info(f"File name: {file_name}")
            file_path = os.path.join(Constants.MINIO_IMAGE_BUCKET, file_name)

            # Upload image to Minio if file is provided. Otherwise, use the generated image.
            agent_avatar = None
            if not file:
                generator = pydenticon.Generator(
                    5,
                    5,
                    digest=hashlib.sha1,
                    foreground=Constants.AGENT_AVATAR_IDENTICON_FOREGROUND_COLOR,
                    background=Constants.AGENT_AVATAR_IDENTICON_BACKGROUND_COLOR,
                )

                # Generate the image
                image_data = generator.generate(
                    data=file_name,
                    width=Constants.AGENT_AVATAR_IDENTICON_WIDTH,
                    height=Constants.AGENT_AVATAR_IDENTICON_HEIGHT,
                    output_format=Constants.AGENT_AVATAR_IDENTICON_OUTPUT_FORMAT,
                )

                # Convert to BinaryIO
                agent_avatar = BytesIO(image_data)
            else:
                agent_avatar = file.file

            # Upload image to Minio
            logger.info(f"Uploading agent avatar to Minio: {file_path}")
            is_file_uploaded = self._minio_connector.upload_files(
                object_name=file_path,
                data=agent_avatar,
                bucket_name=Constants.MINIO_IMAGE_BUCKET,
            )
            if not is_file_uploaded:
                return APIError(kind=ErrorCodesMappingNumber.UNABLE_TO_UPLOAD_FILE_TO_MINIO.value)

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
        self, agent_id: str, agent_request: AgentRequest, user_id: str
    ) -> Optional[APIError]:
        """
        Update an agent.

        Args:
            agent_id (str): Agent id
            agent_request (AgentRequest): Agent request object
            user_id (str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define to-be-updated agent
            agent = agent_request.model_dump(exclude_unset=True)

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
            # Delete agent
            err = self._agent_repo.delete_agent(agent_id=agent_id, user_id=user_id)

        return err if err else None
