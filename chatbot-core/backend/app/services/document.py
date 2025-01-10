import contextlib
import os
from typing import List
from typing import Optional
from typing import Tuple

from fastapi import File
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.databases.minio import MinioConnector
from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.models import Document
from app.repositories.document import DocumentRepository
from app.services.base import BaseService
from app.settings import Constants
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.file import construct_file_path
from app.utils.api.helpers import get_logger
from app.utils.llm.pipeline import index_document_to_vector_db

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
            db_session (Session): Database session
            minio_connector (Optional[MinioConnector]): Object storage connection. Defaults to None.
            qdrant_connector (Optional[QdrantConnector]): Vector database connection. Defaults to None.
            redis_connector (Optional[RedisConnector]): Cache store connection. Defaults to None.
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._document_repo = DocumentRepository(db_session=self._db_session)

        # Define external storage's connectors
        self._minio_connector = minio_connector
        self._qdrant_connector = qdrant_connector
        self._redis_connector = redis_connector

    def upload_documents(
        self, documents: List[UploadFile] = File(...)
    ) -> Tuple[List[str], Optional[APIError]]:
        """
        Upload documents to object storage. Then, trigger the indexing pipeline into the vector database.

        Args:
            documents (List[UploadFile]): List of files to be uploaded.

        Returns:
            Tuple[List[str], Optional[APIError]]: List of document file paths and error if any.
        """
        # Check if files are valid. There are cases where the uploaded file is crashed or empty.
        for document in documents:
            if not document.filename:
                return APIError(kind=ErrorCodesMappingNumber.INVALID_DOCUMENT.value)

        document_urls = []
        try:
            # Upload each file to the object storage
            for document in documents:
                # Automatically closing file after reading
                with contextlib.closing(document.file):
                    # Generate file path
                    object_name, file_extension = os.path.splitext(document.filename)
                    file_path = construct_file_path(
                        object_name=object_name,
                        bucket_name=Constants.MINIO_DOCUMENT_BUCKET,
                        file_extension=file_extension.lstrip("."),
                    )
                    logger.info(f"Uploading document: {document.filename}")

                    with self._transaction():
                        # Write document metadata to database
                        document = Document(
                            name=document.filename,
                            document_url=file_path,
                        )
                        err = self._document_repo.create_document(document=document)
                        if err:
                            return [], err

                    # Upload file to object storage
                    is_file_uploaded = self._minio_connector.upload_file(
                        object_name=file_path,
                        data=document.file,
                        bucket_name=Constants.MINIO_DOCUMENT_BUCKET,
                    )
                    if not is_file_uploaded:
                        return None, APIError(
                            kind=ErrorCodesMappingNumber.UNABLE_TO_UPLOAD_FILE_TO_MINIO.value
                        )

                    # Append document URL to the list
                    document_urls.append(file_path)

                    # # Index document to vector database
                    # index_document_to_vector_db(
                    #     document=document,
                    #     qdrant_connector=self._qdrant_connector,
                    #     redis_connector=self._redis_connector,
                    # )
        except Exception as e:
            logger.error(f"Error uploading documents: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return document_urls, err
