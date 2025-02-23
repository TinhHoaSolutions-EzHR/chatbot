from datetime import datetime
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import status
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.databases.minio import get_minio_connector
from app.databases.minio import MinioConnector
from app.databases.mssql import get_db_session
from app.models.document import DocumentUploadResponse
from app.services.document import DocumentService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def upload_documents(
    issue_date: datetime = Form(default_factory=datetime.now),
    uploaded_documents: List[UploadFile] = File(...),
    db_session: Session = Depends(get_db_session),
    minio_connector: MinioConnector = Depends(get_minio_connector),
) -> BackendAPIResponse:
    """
    Upload documents to object storage. Then, trigger the indexing pipeline into the vector database.

    Args:
        issue_date (datetime): Issue date of the document. Defaults to the current date.
        uploaded_documents (List[UploadFile]): List of documents to upload.
        db_session (Session): Database session. Defaults to relational database session.
        minio_connector (MinioConnector): MinIO connector.

    Returns:
        BackendAPIResponse: API response with the uploaded document URLs.
    """
    # Upload documents to object storage and trigger indexing pipeline
    uploaded_document_results, err = DocumentService(
        db_session=db_session,
        minio_connector=minio_connector,
    ).upload_documents(issue_date=issue_date, uploaded_documents=uploaded_documents)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    if uploaded_document_results:
        data = [
            DocumentUploadResponse(task_id=task_id, document_url=document_url)
            for document_url, task_id in uploaded_document_results
        ]
    else:
        data = []

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )
