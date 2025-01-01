from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import EncryptionKey
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class EncryptionRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Repository class for handling encryption-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_encryption_key(self) -> Tuple[EncryptionKey, Optional[APIError]]:
        """
        Get encryption key.

        Returns:
            str: Encryption key
        """
        try:
            encryption_key = self._db_session.query(EncryptionKey).first()
            return encryption_key, None
        except Exception as e:
            logger.error(f"Error getting encryption key: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def set_encryption_key(self, key: EncryptionKey) -> Optional[APIError]:
        """
        Set encryption key.

        Args:
            key (str): Encryption key
        """
        try:
            self._db_session.add(key)
            return None
        except Exception as e:
            logger.error(f"Error setting encryption key: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
