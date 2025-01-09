from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from app.models import Folder
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class FolderRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Folder repository class for handling folder-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_folders(self, user_id: str) -> Tuple[List[Folder], Optional[APIError]]:
        """
        Get all folders of the user.

        Args:
            user_id (str): User ID

        Returns:
            Tuple[List[Folder], Optional[APIError]]: List of folder objects and APIError object if any error
        """
        try:
            folders = (
                self._db_session.query(Folder)
                .filter(Folder.user_id == user_id)
                .order_by(Folder.created_at.desc())
                .all()
            )
            return folders, None
        except Exception as e:
            logger.error(f"Error getting folders: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_folder(
        self, folder_id: str, user_id: str
    ) -> Tuple[Optional[Folder], Optional[APIError]]:
        """
        Get folder by ID.

        Args:
            folder_id (str): Folder ID
            user_id (str): User ID

        Returns:
            Tuple[Optional[Folder], Optional[APIError]]: Folder object and APIError object if any error
        """
        try:
            folder = (
                self._db_session.query(Folder)
                .options(noload(Folder.chat_sessions))
                .filter(and_(Folder.id == folder_id, Folder.user_id == user_id))
                .first()
            )
            return folder, None
        except Exception as e:
            logger.error(f"Error getting folder: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_folder(self, folder: Folder) -> Optional[APIError]:
        """
        Create a new folder.

        Args:
            folder (Folder): Folder object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(folder)
            return None
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_folder(
        self, folder_id: str, folder: Dict[str, Any], user_id: str
    ) -> Tuple[Optional[Folder], Optional[APIError]]:
        """
        Update folder.

        Args:
            folder_id (str): Folder ID.
            folder (Dict[str, Any]): Folder object.
            user_id (str): User ID.

        Returns:
            Tuple[Optional[Folder], Optional[APIError]]: Folder object and APIError object if any error.
        """
        try:
            # Check if folder exists
            folder_exists = (
                self._db_session.query(Folder)
                .filter(and_(Folder.id == folder_id, Folder.user_id == user_id))
                .first()
            )
            if not folder_exists:
                return APIError(kind=ErrorCodesMappingNumber.FOLDER_NOT_FOUND.value)

            # Update folder
            self._db_session.query(Folder).filter(
                and_(Folder.id == folder_id, Folder.user_id == user_id)
            ).update(folder)

            # Get the updated folder
            updated_folder = (
                self._db_session.query(Folder)
                .filter(and_(Folder.id == folder_id, Folder.user_id == user_id))
                .first()
            )

            return updated_folder, None
        except Exception as e:
            logger.error(f"Error updating folder: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_folder(self, folder_id: str, user_id: str) -> Optional[APIError]:
        """
        Delete folder.

        Args:
            folder_id (str): Folder ID
            user_id (str): User ID

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(Folder).filter(
                and_(Folder.id == folder_id, Folder.user_id == user_id)
            ).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting folder: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
