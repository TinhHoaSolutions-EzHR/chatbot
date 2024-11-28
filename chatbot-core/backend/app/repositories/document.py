from sqlalchemy.orm import Session
from typing import List, Tuple

from app.models.api import APIError
from app.models.document import DocumentMetadata
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class DocumentRepository:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get_documents_metadata(self) -> Tuple[List[DocumentMetadata], APIError | None]:
        """
        Get all documents metadata

        Returns:
            Tuple[List[DocumentMetadata], APIError | None]: List of document metadata objects and APIError object if any error
        """
        try:
            documents = self._db_session.query(DocumentMetadata).all()
            return documents, None
        except Exception as e:
            logger.error(f"Error getting documents: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_document_metadata(self, id: int) -> Tuple[DocumentMetadata, APIError | None]:
        """
        Get document metadata by id

        Args:
            id(int): Document id

        Returns:
            Tuple[DocumentMetadata, APIError | None]: Document metadata object and APIError object if any error
        """
        try:
            document = self._db_session.query(DocumentMetadata).filter(DocumentMetadata.id == id).first()
            if not document:
                return None, APIError(kind=ErrorCodesMappingNumber.NOT_FOUND.value)
            return document, None
        except Exception as e:
            logger.error(f"Error getting document: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

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

    def update_document_metadata(self, id: int, document_metadata: DocumentMetadata) -> APIError | None:
        """
        Update an existing document metadata

        Args:
            id(int): Document id
            document(DocumentMetadata): Document metadata object

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            document_metadata = {
                key: value for key, value in document_metadata.__dict__.items() if not key.startswith("_")
            }
            self._db_session.query(DocumentMetadata).filter(DocumentMetadata.id == id).update(document_metadata)
            self._db_session.commit()
            return None
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_document_metadata(self, id: int) -> APIError | None:
        """
        Delete document metadata

        Args:
            id(int): Document id

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            self._db_session.query(DocumentMetadata).filter(DocumentMetadata.id == id).delete()
            self._db_session.commit()
            return None
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
