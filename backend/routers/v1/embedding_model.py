from fastapi import APIRouter, status

from services.embedding_model import EmbeddingModelService
from utils import logger
from utils.create_api_response import BackendAPIResponse

# I will switch to use dependency injection later
from main import postgres_instance

logger = logger.LoggerFactory(__name__).get_logger()

router = APIRouter(prefix="/embedding_model", tags=["embedding_model"])


@router.get("/", response_model=BackendAPIResponse)
async def get_embedding_models(limit: int = 10, offset: int = 0):
    """
    Get all embedding models
    """
    # Get embedding models
    embedding_models, err = EmbeddingModelService(db_session=postgres_instance).get_embedding_models(
        limit=limit, offset=offset
    )
    if err:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = err.detail
    else:
        status_code = status.HTTP_200_OK
        message = "Embedding models found"
    
    # Return response 
    BackendAPIResponse().set_status_code(
        status_code
    ).set_message(message).set_data(embedding_models).respond()