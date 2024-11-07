from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from services.embedding_model import EmbeddingModelService
from databases.postgres import get_session
from models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelRequest,
    EmbeddingModelResponse,
)
from models.api import APIResponse
from utils.logger import LoggerFactory
from utils.api_response import handle_api_response


logger = LoggerFactory().get_logger(__name__)
router = APIRouter(prefix="/embedding_model", tags=["embedding_model"])


@router.get("/", response_model=APIResponse)
async def get_embedding_models(db_session: Session = Depends(get_session)):
    """
    Get all embedding models
    """
    # Get embedding models
    embedding_models, err = EmbeddingModelService(
        db_session=db_session
    ).get_embedding_models()
    return handle_api_response(
        data=embedding_models,
        err=err,
        success_status_code=status.HTTP_200_OK,
        model_response=EmbeddingModelResponse,
    )


@router.get("/{id}", response_model=APIResponse)
async def get_embedding_model_by_id(
    id: int, db_session: Session = Depends(get_session)
):
    """
    Get embedding model by id
    """
    # Get embedding model by id
    embedding_model, err = EmbeddingModelService(
        db_session=db_session
    ).get_embedding_model(id=id)
    return handle_api_response(
        data=embedding_model,
        err=err,
        success_status_code=status.HTTP_200_OK,
        model_response=EmbeddingModelResponse,
    )


@router.post("/", response_model=APIResponse)
async def create_embedding_model(
    embedding_model_request: EmbeddingModelRequest,
    db_session: Session = Depends(get_session),
):
    """
    Create embedding model
    """
    # Define embedding model
    embedding_model = EmbeddingModel(
        name=embedding_model_request.name,
        description=embedding_model_request.description,
        provider=embedding_model_request.provider,
    )

    # Create embedding model
    err = EmbeddingModelService(db_session=db_session).create_embedding_model(
        embedding_model
    )
    return handle_api_response(
        data=embedding_model,
        err=err,
        success_status_code=status.HTTP_201_CREATED,
        model_response=EmbeddingModelResponse,
    )


@router.put("/{id}", response_model=APIResponse)
async def update_embedding_model(
    id: int,
    embedding_model_request: EmbeddingModelRequest,
    db_session: Session = Depends(get_session),
):
    """
    Update embedding model
    """
    # Define embedding model
    embedding_model = EmbeddingModel(
        name=embedding_model_request.name,
        description=embedding_model_request.description,
        provider=embedding_model_request.provider,
    )

    # Update embedding model
    err = EmbeddingModelService(db_session=db_session).update_embedding_model(
        id=id, embedding_model=embedding_model
    )
    return handle_api_response(
        data=embedding_model,
        err=err,
        success_status_code=status.HTTP_200_OK,
        model_response=EmbeddingModelResponse,
    )


@router.delete("/{id}", response_model=APIResponse)
async def delete_embedding_model(id: int, db_session: Session = Depends(get_session)):
    """
    Delete embedding model by id
    """
    # Delete embedding model by id
    err = EmbeddingModelService(db_session=db_session).delete_embedding_model(id=id)
    return handle_api_response(
        data=None,
        err=err,
        success_status_code=status.HTTP_204_NO_CONTENT,
        model_response=None,
    )
