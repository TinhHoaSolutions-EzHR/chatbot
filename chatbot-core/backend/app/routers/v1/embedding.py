from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models.embedding import EmbeddingModelRequest
from app.models.embedding import EmbeddingModelResponse
from app.services.embedding import EmbeddingModelService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.helpers import get_logger


logger = get_logger(__name__)
router = APIRouter(prefix="/embedding-models", tags=["embedding", "provider", "model"])


@router.get("", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_embedding_models(db_session: Session = Depends(get_db_session)) -> BackendAPIResponse:
    """
    Get all embedding models of the application.

    Args:
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Get embedding models of the application
    embedding_models, err = EmbeddingModelService(db_session=db_session).get_embedding_models()
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse embedding models
    if embedding_models:
        data = [
            EmbeddingModelResponse.model_validate(embedding_model)
            for embedding_model in embedding_models
        ]
    else:
        data = []

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.get("/{embedding_model_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_embedding_model(
    embedding_model_id: int, db_session: Session = Depends(get_db_session)
) -> BackendAPIResponse:
    """
    Get embedding model by ID.

    Args:
        embedding_model_id (int): Embedding model ID
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Get embedding model by ID
    embedding_model, err = EmbeddingModelService(db_session=db_session).get_embedding_model(
        embedding_model_id=embedding_model_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse embedding model
    if embedding_model:
        data = EmbeddingModelResponse.model_validate(embedding_model)
    else:
        data = None

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_embedding_model(
    embedding_model_request: EmbeddingModelRequest, db_session: Session = Depends(get_db_session)
) -> BackendAPIResponse:
    """
    Create a new embedding model.

    Args:
        embedding_model_request (EmbeddingModelRequest): Embedding model request object
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Create embedding model
    err = EmbeddingModelService(db_session=db_session).create_embedding_model(
        embedding_model_request=embedding_model_request
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = embedding_model_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.put("/{embedding_model_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_embedding_model(
    embedding_model_id: int,
    embedding_model_request: EmbeddingModelRequest,
    db_session: Session = Depends(get_db_session),
) -> BackendAPIResponse:
    """
    Update embedding model by ID.

    Args:
        embedding_model_id (int): Embedding model ID
        embedding_model_request (EmbeddingModelRequest): Embedding model request object
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Update embedding model by ID
    err = EmbeddingModelService(db_session=db_session).update_embedding_model(
        embedding_model_id=embedding_model_id, embedding_model_request=embedding_model_request
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = embedding_model_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.delete("/{embedding_model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_embedding_model(embedding_model_id: int, db_session: Session = Depends(get_db_session)):
    """
    Delete embedding model by ID.

    Args:
        embedding_model_id (int): Embedding model ID
        db_session (Session): Database session. Defaults to relational database session.
    """
    # Delete embedding model by ID
    err = EmbeddingModelService(db_session=db_session).delete_embedding_model(
        embedding_model_id=embedding_model_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)
