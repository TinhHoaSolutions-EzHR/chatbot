from sqlalchemy.orm import Session
from typing import List, Tuple

from app.models.api import APIError
from app.models.document import DocumentMetadata
from app.repositories.base import BaseRepository
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class DocumentRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session=db_session)

    def create_document_metadata(self, document_metadata: DocumentMetadata) -> APIError | None:
        """
        Create document metadata

        Args:
            document(DocumentMetadata): Document metadata object

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            self._db_session.add(document_metadata)
            self._db_session.commit()
            return None
        except Exception as e:
            logger.error(f"Error creating document: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
