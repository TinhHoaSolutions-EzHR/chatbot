from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import EmbeddingModel
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class EmbeddingModelRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Embedding model repository class for handling embedding model-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_embedding_models(self) -> Tuple[List[EmbeddingModel], Optional[APIError]]:
        """
        Get all embedding models.

        Returns:
            Tuple[List[EmbeddingModel], Optional[APIError]]: List of embedding model objects and APIError object if any error
        """
        try:
            embedding_models = self._db_session.query(EmbeddingModel).all()
            return embedding_models, None
        except Exception as e:
            logger.error(f"Error getting embedding models: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_embedding_model(
        self, embedding_model_id: str
    ) -> Tuple[Optional[EmbeddingModel], Optional[APIError]]:
        """
        Get an embedding model by id.

        Args:
            embedding_model_id (str): Embedding model id

        Returns:
            Tuple[Optional[EmbeddingModel], Optional[APIError]]: Embedding model object and APIError object if any error
        """
        try:
            embedding_model = (
                self._db_session.query(EmbeddingModel)
                .filter(EmbeddingModel.id == embedding_model_id)
                .first()
            )
            return embedding_model, None
        except Exception as e:
            logger.error(f"Error getting embedding model: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_embedding_model(self, embedding_model: EmbeddingModel) -> Optional[APIError]:
        """
        Create an embedding model.

        Args:
            embedding_model (EmbeddingModel): Embedding model object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(embedding_model)
            return None
        except Exception as e:
            logger.error(f"Error creating embedding model: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_embedding_model(
        self, embedding_model_id: str, embedding_model: Dict[str, Any]
    ) -> Optional[APIError]:
        """
        Update an embedding model.

        Args:
            embedding_model_id (str): Embedding model id
            embedding_model (Dict[str, Any]): Embedding model data

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(EmbeddingModel).filter(
                EmbeddingModel.id == embedding_model_id
            ).update(embedding_model)
            return None
        except Exception as e:
            logger.error(f"Error updating embedding model: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_embedding_model(self, embedding_model_id: str) -> Optional[APIError]:
        """
        Delete an embedding model.

        Args:
            embedding_model_id (str): Embedding model id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(EmbeddingModel).filter(
                EmbeddingModel.id == embedding_model_id
            ).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting embedding model: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
