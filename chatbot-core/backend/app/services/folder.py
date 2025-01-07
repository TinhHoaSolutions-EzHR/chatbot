from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import Folder
from app.models.folder import FolderRequest
from app.repositories.chat import ChatRepository
from app.repositories.folder import FolderRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class FolderService(BaseService):
    def __init__(self, db_session: Session):
        """
        Folder service class for handling folder-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._folder_repo = FolderRepository(db_session=db_session)
        self._chat_repo = ChatRepository(db_session=db_session)

    def get_folders(self, user_id: str) -> Tuple[List[Folder], Optional[APIError]]:
        """
        Get all folders of the user.

        Args:
            user_id (str): User ID
        """
        folders, err = self._folder_repo.get_folders(user_id=user_id)
        if err:
            return [], err

        if folders:
            # Get chat sessions for each folder
            for folder in folders:
                chat_sessions, err = self._chat_repo.get_chat_sessions(
                    user_id=user_id, folder_id=folder.id
                )
                if err:
                    return [], err

                folder.chat_sessions = chat_sessions

        return folders, None

    def create_folder(self, folder_request: FolderRequest, user_id: str) -> Optional[APIError]:
        """
        Create a new folder.

        Args:
            folder_request (FolderRequest): Folder request object
            user_id (str): User ID

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define folder
            folder = Folder(user_id=user_id, name=folder_request.name)

            # Create folder
            err = self._folder_repo.create_folder(folder=folder)

        return err if err else None

    def update_folder(
        self, folder_id: str, folder_request: FolderRequest, user_id: str
    ) -> Optional[APIError]:
        """
        Update an existing folder.

        Args:
            folder_id (str): Folder ID
            folder_request (FolderRequest): Folder request object
            user_id (str): User ID

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define to-be-updated folder
            folder = folder_request.model_dump(exclude_unset=True, exclude_defaults=True)

            # Update folder
            err = self._folder_repo.update_folder(
                folder_id=folder_id, folder=folder, user_id=user_id
            )

        return err if err else None

    def delete_folder(self, folder_id: str, user_id: str) -> Optional[APIError]:
        """
        Delete a folder.

        Args:
            folder_id (str): Folder ID
            user_id (str): User ID

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Delete folder
            err = self._folder_repo.delete_folder(folder_id=folder_id, user_id=user_id)

        return err if err else None
