from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models.llm import LLMModelRequest
from app.models.llm import LLMModelResponse
from app.services.llm import LLMModelService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/llm-models", tags=["llm", "provider", "model"])


@router.get("", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_llm_models(db_session: Session = Depends(get_db_session)) -> BackendAPIResponse:
    """
    Get all LLM models of the application.

    Args:
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Get LLM models of the application
    llm_models, err = LLMModelService(db_session=db_session).get_llm_models()
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse LLM models
    if llm_models:
        data = [LLMModelResponse.model_validate(llm_model) for llm_model in llm_models]
    else:
        data = []

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.get("/{llm_model_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_llm_model(
    llm_model_id: int, db_session: Session = Depends(get_db_session)
) -> BackendAPIResponse:
    """
    Get LLM model by ID.

    Args:
        llm_model_id (int): LLM model ID
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Get LLM model by ID
    llm_model, err = LLMModelService(db_session=db_session).get_llm_model(llm_model_id=llm_model_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=LLMModelResponse.model_validate(llm_model))
        .respond()
    )


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_llm_model(
    llm_model_request: LLMModelRequest, db_session: Session = Depends(get_db_session)
) -> BackendAPIResponse:
    """
    Create LLM model.

    Args:
        llm_model_request (LLMModelRequest): LLM model request
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Create LLM model
    llm_model, err = LLMModelService(db_session=db_session).create_llm_model(
        llm_model_request=llm_model_request
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=LLMModelResponse.model_validate(llm_model))
        .respond()
    )


@router.put("/{llm_model_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_llm_model(
    llm_model_id: int,
    llm_model_request: LLMModelRequest,
    db_session: Session = Depends(get_db_session),
) -> BackendAPIResponse:
    """
    Update LLM model.

    Args:
        llm_model_id (int): LLM model ID
        llm_model_request (LLMModelRequest): LLM model request
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Update LLM model
    llm_model, err = LLMModelService(db_session=db_session).update_llm_model(
        llm_model_id=llm_model_id, llm_model_request=llm_model_request
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=LLMModelResponse.model_validate(llm_model))
        .respond()
    )


@router.delete("/{llm_model_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def delete_llm_model(
    llm_model_id: int, db_session: Session = Depends(get_db_session)
) -> BackendAPIResponse:
    """
    Delete LLM model by ID.

    Args:
        llm_model_id (int): LLM model ID
        db_session (Session): Database session. Defaults to relational database session.

    Returns:
        BackendAPIResponse: API response
    """
    # Delete LLM model by ID
    err = LLMModelService(db_session=db_session).delete_llm_model(llm_model_id=llm_model_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).respond()
