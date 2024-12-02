from typing import Annotated
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import status
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models.api import APIResponse
from app.models.connector import ConnectorRequest
from app.models.connector import ConnectorResponse
from app.models.document import DocumentUploadResponse
from app.services.connector import ConnectorService
from app.services.document import DocumentService
from app.settings import Constants
from app.utils.api_response import BackendAPIResponse
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)
router = APIRouter(prefix="/connectors", tags=["connectors", "documents"])


@router.post("/documents/upload", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def upload_documents(
    documents: Annotated[List[UploadFile], File(description="One or multiple documents")],
    db_session: Session = Depends(get_db_session),
) -> None:
    """
    Upload documents to object storage. Then, trigger the indexing pipeline into the vector database.

    Args:
        files (List[UploadFile]): List of files to be uploaded.
        db_session (Session, optional): Database session. Defaults to relational database engine.
    """
    # Upload documents to object storage and trigger indexing pipeline
    document_urls, err = DocumentService(db_session=db_session).upload_documents(documents=documents)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = [DocumentUploadResponse(document_url=document_url) for document_url in document_urls]

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=data).respond()


@router.get("", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_connectors(db_session: Session = Depends(get_db_session)) -> None:
    """
    Get all connectors.

    Args:
        db_session (Session, optional): Database session. Defaults to relational database engine.
    """
    # Get connectors
    connectors, err = ConnectorService(db_session=db_session).get_connectors()
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = [ConnectorResponse.model_validate(connector) for connector in connectors]

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=data).respond()


@router.get("/{connector_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_connector(connector_id: str, db_session: Session = Depends(get_db_session)) -> None:
    """
    Get connector by id.

    Args:
        connector_id (str): Connector id
        db_session (Session, optional): Database session. Defaults to relational database engine.
    """
    # Get connector by id
    connector, err = ConnectorService(db_session=db_session).get_connector(connector_id=connector_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    if connector:
        data = ConnectorResponse.model_validate(connector)
    else:
        data = None

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=data).respond()


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_connector(connector_request: ConnectorRequest, db_session: Session = Depends(get_db_session)) -> None:
    """
    Create connector.

    Args:
        name (str): Connector name
        db_session (Session, optional): Database session. Defaults to relational database engine.
    """
    # Create connector
    err = ConnectorService(db_session=db_session).create_connector(connector_request=connector_request)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = connector_request.model_dump(exclude_unset=True)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=data).respond()


@router.patch("/{connector_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_connector(
    connector_id: str, connector_request: ConnectorRequest, db_session: Session = Depends(get_db_session)
) -> None:
    """
    Update connector by connector_id.

    Args:
        connector_id (int): Connector id
        name (str): Connector name
        db_session (Session, optional): Database session. Defaults to relational database engine.
    """
    # Update connector
    err = ConnectorService(db_session=db_session).update_connector(
        connector_id=connector_id, connector_request=connector_request
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = connector_request.model_dump(exclude_unset=True)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=data).respond()


@router.delete("/{connector_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connector(connector_id: str, db_session: Session = Depends(get_db_session)) -> None:
    """
    Delete connector by connector_id.

    Args:
        connector_id (str): Connector id
        db_session (Session, optional): Database session. Defaults to relational database engine.
    """
    # Delete connector by id
    err = ConnectorService(db_session=db_session).delete_connector(connector_id=connector_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)
