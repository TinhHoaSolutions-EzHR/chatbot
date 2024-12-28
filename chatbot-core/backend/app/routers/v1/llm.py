from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models.llm import LLMProviderRequest
from app.models.llm import LLMProviderResponse
from app.services.llm import LLMProviderService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/providers/llm", tags=["llm", "provider", "model"])


@router.get("", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_llm_providers(
    db_session: Session = Depends(get_db_session),
) -> BackendAPIResponse:
    """
    Get all llm providers of the application.

    Args:
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Get llm providers of the application
    llm_providers, err = LLMProviderService(db_session=db_session).get_llm_providers()
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse llm providers
    if llm_providers:
        data = [LLMProviderResponse.model_validate(llm_provider) for llm_provider in llm_providers]
    else:
        data = []

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.get("/{llm_provider_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_llm_provider(
    llm_provider_id: str, db_session: Session = Depends(get_db_session)
) -> BackendAPIResponse:
    """
    Get llm provider by ID.

    Args:
        llm_provider_id (str): The provider ID.
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Get llm provider
    llm_provider, err = LLMProviderService(db_session=db_session).get_llm_provider(
        llm_provider_id=llm_provider_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse llm provider
    if llm_provider:
        data = LLMProviderResponse.model_validate(llm_provider)
    else:
        data = None

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_llm_provider(
    llm_provider_request: LLMProviderRequest, db_session: Session = Depends(get_db_session)
) -> BackendAPIResponse:
    """
    Create a new llm provider.

    Args:
        llm_provider_request (LLMProviderRequest): LLM provider request object.
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Create llm provider
    err = LLMProviderService(db_session=db_session).create_llm_provider(
        llm_provider_request=llm_provider_request
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = llm_provider_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.patch("/{llm_provider_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_llm_provider(
    llm_provider_id: str,
    llm_provider_request: LLMProviderRequest,
    db_session: Session = Depends(get_db_session),
) -> BackendAPIResponse:
    """
    Update llm provider by ID.

    Args:
        llm_provider_id (str): The provider ID.
        llm_provider_request (LLMProviderRequest): LLM provider request object.
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Update llm provider
    err = LLMProviderService(db_session=db_session).update_llm_provider(
        llm_provider_id=llm_provider_id, llm_provider_request=llm_provider_request
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = llm_provider_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.delete("/{llm_provider_id}", status_code=status.HTTP_200_OK)
def delete_llm_provider(
    llm_provider_id: str, db_session: Session = Depends(get_db_session)
) -> None:
    """
    Delete llm provider by ID.

    Args:
        llm_provider_id (str): The provider ID.
        db_session (Session): Database session. Defaults to relational database session.
    """
    # Delete llm provider
    err = LLMProviderService(db_session=db_session).delete_llm_provider(
        llm_provider_id=llm_provider_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)
