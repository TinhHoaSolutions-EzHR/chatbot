from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models.embedding import EmbeddingProviderRequest
from app.models.embedding import EmbeddingProviderResponse
from app.services.embedding import EmbeddingProviderService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.helpers import get_logger


logger = get_logger(__name__)
router = APIRouter(prefix="/providers/embeddings", tags=["embedding", "provider", "model"])


@router.get("", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_embedding_providers(db_session: Session = Depends(get_db_session)) -> BackendAPIResponse:
    """
    Get all embedding providers of the application.

    Args:
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Get embedding providers of the application
    embedding_providers, err = EmbeddingProviderService(
        db_session=db_session
    ).get_embedding_providers()
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse embedding providers
    if embedding_providers:
        data = [
            EmbeddingProviderResponse.model_validate(embedding_provider)
            for embedding_provider in embedding_providers
        ]
    else:
        data = []

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.get("/{embedding_provider_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_embedding_provider(
    embedding_provider_id: str, db_session: Session = Depends(get_db_session)
) -> BackendAPIResponse:
    """
    Get embedding provider by ID.

    Args:
        embedding_provider_id (str): Embedding provider ID.
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response.
    """
    # Get embedding provider by ID
    embedding_provider, err = EmbeddingProviderService(
        db_session=db_session
    ).get_embedding_provider(embedding_provider_id=embedding_provider_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse embedding provider
    if embedding_provider:
        data = EmbeddingProviderResponse.model_validate(embedding_provider)
    else:
        data = None

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.patch(
    "/{embedding_provider_id}", response_model=APIResponse, status_code=status.HTTP_200_OK
)
def update_embedding_provider(
    embedding_provider_id: str,
    embedding_provider_request: EmbeddingProviderRequest,
    db_session: Session = Depends(get_db_session),
) -> BackendAPIResponse:
    """
    Update embedding provider by ID.

    Args:
        embedding_provider_id (str): Embedding provider ID.
        embedding_provider_request (EmbeddingProviderRequest): Embedding provider request object.
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Update embedding provider by ID
    err = EmbeddingProviderService(db_session=db_session).update_embedding_provider(
        embedding_provider_id=embedding_provider_id,
        embedding_provider_request=embedding_provider_request,
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = embedding_provider_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )
