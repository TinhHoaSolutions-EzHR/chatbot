import os
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.databases.minio import get_object_storage_client
from app.models.api import APIError
from app.models.document import DocumentMetadata
from app.repositories.document import DocumentRepository
from app.settings import Constants
from app.utils.accents_handler import remove_vietnamese_accents
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.indexing import index_document_to_vector_db
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class DocumentService:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def upload_documents(
        self,
        files: Annotated[List[UploadFile], File(description="One or multiple documents")],
    ) -> APIError | None:
        """
        Upload documents to object storage. Then, trigger the indexing pipeline into the vector database.
        """
        # Check if files are empty
        for file in files:
            if not file.filename:
                return APIError(kind=ErrorCodesMappingNumber.INVALID_REQUEST)

        err = None
        try:
            # Get the object storage connection
            object_storage = get_object_storage_client()

            # Upload files to Minio
            for file in files:
                # Begin transaction
                self._db_session.begin()

                file_name = remove_vietnamese_accents(input_str=file.filename).replace(" ", "_").lower()
                file_path = os.path.join(Constants.MINIO_DOCUMENT_BUCKET, file_name)

                logger.info(f"Uploading document: {file.filename}")

                # Write document metadata to database
                document_metadata = DocumentMetadata(
                    name=file.filename,
                    object_url=file_path,
                )
                err = DocumentRepository(db_session=self._db_session).create_document_metadata(
                    document_metadata=document_metadata
                )

                # Commit transaction
                self._db_session.commit()

                # Upload file to object storage
                object_storage.upload_files(
                    object_name=file_path,
                    data=file.file,
                    bucket_name=Constants.MINIO_DOCUMENT_BUCKET,
                )

                # Index document to vector database
                index_document_to_vector_db(file=file)
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error uploading documents: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err
