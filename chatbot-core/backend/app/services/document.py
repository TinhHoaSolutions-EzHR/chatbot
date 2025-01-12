import contextlib
import os
from datetime import datetime
from typing import List
from typing import Optional
from typing import Tuple

from fastapi import File
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.databases.minio import MinioConnector
from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.integrations.llama_index.ingestion_pipelines import IndexingPipeline
from app.models import Document
from app.repositories.document import DocumentRepository
from app.services.base import BaseService
from app.settings import Constants
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.file import construct_file_path
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class DocumentService(BaseService):
    def __init__(
        self,
        db_session: Session,
        minio_connector: Optional[MinioConnector] = None,
        qdrant_connector: Optional[QdrantConnector] = None,
        redis_connector: Optional[RedisConnector] = None,
    ) -> None:
        """
        Document service class for handling document-related operations.

        Args:
            db_session (Session): Database session.
            minio_connector (Optional[MinioConnector]): Object storage connection. Defaults to None.
            qdrant_connector (Optional[QdrantConnector]): Vector database connection. Defaults to None.
            redis_connector (Optional[RedisConnector]): Cache store connection. Defaults to None.
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._document_repo = DocumentRepository(db_session=self._db_session)

        # Define external storage's connectors
        self._minio_connector = minio_connector

        # Define indexing pipeline
        self._indexing_pipeline = IndexingPipeline(
            qdrant_connector=qdrant_connector,
            redis_connector=redis_connector,
        )

    def _validate_documents(self, documents: List[UploadFile]) -> Optional[APIError]:
        """
        Validate uploaded documents.

        Args:
            documents: List of uploaded files to validate.

        Returns:
            Optional[APIError]: Error if validation fails, None otherwise.
        """
        for document in documents:
            if not document.filename:
                return APIError(kind=ErrorCodesMappingNumber.INVALID_DOCUMENT.value)
        return None

    def _store_document(
        self, uploaded_document: UploadFile, issue_date: datetime, is_outdated: bool
    ) -> Tuple[Optional[str], Optional[APIError]]:
        """
        Store a single document in storage and databases.

        Args:
            uploaded_document: File to be stored.
            issue_date: Issue date of the document.
            is_outdated: Flag indicating if the document is outdated.

        Returns:
            Tuple containing the document URL (if successful) and any error.
        """
        object_name, file_extension = os.path.splitext(uploaded_document.filename)
        logger.info(object_name)
        file_path = construct_file_path(
            object_name=object_name,
            bucket_name=Constants.MINIO_DOCUMENT_BUCKET,
            file_extension=file_extension.lstrip("."),
        )
        logger.info(f"Uploading document: {uploaded_document.filename}")

        with self._transaction():
            document = Document(
                name=uploaded_document.filename,
                url=file_path,
            )
            if err := self._document_repo.create_document(document=document):
                return None, err

        if not self._minio_connector.upload_file(
            object_name=file_path,
            data=uploaded_document.file,
            bucket_name=Constants.MINIO_DOCUMENT_BUCKET,
        ):
            return None, APIError(kind=ErrorCodesMappingNumber.UNABLE_TO_UPLOAD_FILE_TO_MINIO.value)

        logger.info(f"Document uploaded: {uploaded_document.filename}")

        # Index the document into the vector database
        metadata = {
            "issue_date": issue_date.strftime(Constants.DATETIME_FORMAT),
            "is_outdated": is_outdated,
        }
        self._indexing_pipeline.run(document=uploaded_document, metadata=metadata)

        return file_path, None

    def upload_documents(
        self,
        issue_date: datetime = datetime.now(),
        is_outdated: bool = True,
        uploaded_documents: List[UploadFile] = File(...),
    ) -> Tuple[List[str], Optional[APIError]]:
        """
        Upload documents to object storage. Then, trigger the indexing pipeline into the vector database.

        Args:
            issue_date (datetime): Issue date of the document.
            is_outdated (bool): Flag to indicate if the document is outdated. Defaults to True.
            uploaded_documents (List[UploadFile]): List of files to be uploaded.

        Returns:
            Tuple[List[str], Optional[APIError]]: List of document file paths and error if any.
        """
        # Check if files are valid. There are cases where the uploaded file is crashed or empty.
        if err := self._validate_documents(documents=uploaded_documents):
            return [], err

        document_urls: List[str] = []
        try:
            for uploaded_document in uploaded_documents:
                with contextlib.closing(uploaded_document.file):
                    document_url, err = self._store_document(
                        uploaded_document=uploaded_document,
                        issue_date=issue_date,
                        is_outdated=is_outdated,
                    )
                    if err:
                        return [], err
                    document_urls.append(document_url)

            return document_urls, None
        except Exception as e:
            logger.error(f"Error uploading documents: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
