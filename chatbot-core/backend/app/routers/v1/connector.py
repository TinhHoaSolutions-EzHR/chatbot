from typing import Annotated, List
from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, status
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models.api import APIResponse
from app.models.connector import ConnectorRequest, ConnectorResponse
from app.models.document import DocumentMetadataResponse
from app.services.connector import ConnectorService
from app.services.document import DocumentService
from app.settings import Constants
from app.utils.api_response import BackendAPIResponse
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)
router = APIRouter(prefix="/connectors", tags=["connectors", "files"])


@router.post("/files/upload", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def upload_documents(
    files: Annotated[List[UploadFile], File(description="One or multiple documents")],
    db_session: Session = Depends(get_db_session),
) -> None:
    """
    Upload documents to object storage. Then, trigger the indexing pipeline into the vector database.

    Args:
        files (List[UploadFile]): List of files to be uploaded.
        db_session (Session, optional): Database session. Defaults to relational database engine.
    """
    # Upload documents to object storage and trigger indexing pipeline
    err = DocumentService(db_session=db_session).upload_documents(files=files)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = [DocumentMetadataResponse(name=file.filename) for file in files]
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
def get_connector(connector_id: int, db_session: Session = Depends(get_db_session)) -> None:
    """
    Get connector by id.

    Args:
        connector_id (int): Connector id
        db_session (Session, optional): Database session. Defaults to relational database engine.
    """
    # Get connector by id
    connector, err = ConnectorService(db_session=db_session).get_connector(connector_id=connector_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = ConnectorResponse.model_validate(connector)

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

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).respond()


@router.patch("/{connector_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_connector(
    connector_id: int, connector_request: ConnectorRequest, db_session: Session = Depends(get_db_session)
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

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).respond()


@router.delete("/{connector_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connector(connector_id: int, db_session: Session = Depends(get_db_session)) -> None:
    """
    Delete connector by connector_id.

    Args:
        connector_id (int): Connector id
        db_session (Session, optional): Database session. Defaults to relational database engine.
    """
    # Delete connector by id
    err = ConnectorService(db_session=db_session).delete_connector(connector_id=connector_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)
