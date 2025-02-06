from typing import Optional

from sqlalchemy.orm import Session

from app.models import Document
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class DocumentRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Document repository class for handling document-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def create_document(self, document: Document) -> Optional[APIError]:
        """
        Create document.

        Args:
            document(Document): Document object.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        try:
            self._db_session.add(document)
            return None
        except Exception as e:
            logger.error(f"Error creating document: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
