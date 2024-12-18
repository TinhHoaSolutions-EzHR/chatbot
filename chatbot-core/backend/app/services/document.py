import contextlib
import os
from typing import Annotated
from typing import List
from typing import Optional
from typing import Tuple

from fastapi import File
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.databases.minio import MinioConnector
from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.models.document import DocumentMetadata
from app.repositories.document import DocumentRepository
from app.services.base import BaseService
from app.settings import Constants
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger
from app.utils.api.helpers import remove_vietnamese_accents
from app.utils.llm.pipeline import index_document_to_vector_db

logger = get_logger(__name__)


class DocumentService(BaseService):
    def __init__(
        self,
        db_session: Session,
        minio_connector: MinioConnector | None = None,
        qdrant_connector: QdrantConnector | None = None,
        redis_connector: RedisConnector | None = None,
    ) -> None:
        """
        Document service class for handling document-related operations.

        Args:
            db_session (Session): Database session
            minio_connector (MinioConnector, optional): Object storage connection. Defaults to None.
            qdrant_connector (QdrantConnector, optional): Vector database connection. Defaults to None.
            redis_connector (RedisConnector, optional): Cache store connection. Defaults to None.
        """
        if minio_connector and not isinstance(minio_connector, MinioConnector):
            raise ValueError("Invalid Minio connector")
        if qdrant_connector and not isinstance(qdrant_connector, QdrantConnector):
            raise ValueError("Invalid Qdrant connector")
        if redis_connector and not isinstance(redis_connector, RedisConnector):
            raise ValueError("Invalid Redis connector")

        super().__init__(db_session=db_session)

        # Define storage connections
        self._minio_connector = minio_connector
        self._qdrant_connector = qdrant_connector
        self._redis_connector = redis_connector

        # Define repositories
        self._document_repo = DocumentRepository(db_session=self._db_session)

    def upload_documents(
        self,
        documents: Annotated[List[UploadFile], File(description="One or multiple documents")],
    ) -> Tuple[List[str], Optional[APIError]]:
        """
        Upload documents to object storage. Then, trigger the indexing pipeline into the vector database.

        Args:
            documents (List[UploadFile]): List of documents to be uploaded.

        Returns:
            Tuple[List[str], Optional[APIError]]: List of document file paths and error if any.
        """
        # Check if files are empty
        for document in documents:
            if not document.filename:
                return APIError(kind=ErrorCodesMappingNumber.INVALID_REQUEST)

        err = None
        deduped_document_urls = []
        try:
            # Upload files to Minio
            for document in documents:
                # Auto close file after reading
                with contextlib.closing(document.file):
                    # Generate file name
                    file_name = (
                        remove_vietnamese_accents(input_str=document.filename)
                        .replace(" ", "_")
                        .lower()
                    )
                    file_path = os.path.join(Constants.MINIO_DOCUMENT_BUCKET, file_name)

                    logger.info(f"Uploading document: {document.filename}")

                    with self._transaction():
                        # Write document metadata to database
                        document_metadata = DocumentMetadata(
                            name=document.filename,
                            document_url=file_path,
                        )
                        err = self._document_repo.create_document_metadata(
                            document_metadata=document_metadata
                        )

                    # Upload file to object storage
                    self._minio_connector.upload_files(
                        object_name=file_path,
                        data=document.file,
                        bucket_name=Constants.MINIO_DOCUMENT_BUCKET,
                    )

                    # Append file path to list
                    if file_path not in deduped_document_urls:
                        deduped_document_urls.append(file_path)

                    # Index document to vector database
                    index_document_to_vector_db(
                        document=document,
                        qdrant_connector=self._qdrant_connector,
                        redis_connector=self._redis_connector,
                    )
        except Exception as e:
            logger.error(f"Error uploading documents: {e}", exc_info=True)
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return deduped_document_urls, err
