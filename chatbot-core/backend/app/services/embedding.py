from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import EmbeddingModel
from app.models.embedding import EmbeddingModelRequest
from app.repositories.embedding import EmbeddingModelRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class EmbeddingModelService(BaseService):
    def __init__(self, db_session: Session):
        """
        Embedding model service class for handling embedding model-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._embedding_model_repo = EmbeddingModelRepository(db_session=db_session)

    def get_embedding_models(self) -> Tuple[List[EmbeddingModel], Optional[APIError]]:
        """
        Get all embedding models.

        Returns:
            Tuple[List[EmbeddingModel], Optional[APIError]]: List of embedding model objects and APIError object if any error
        """
        return self._embedding_model_repo.get_embedding_models()

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
        return self._embedding_model_repo.get_embedding_model(embedding_model_id=embedding_model_id)

    def create_embedding_model(
        self, embedding_model_request: EmbeddingModelRequest
    ) -> Optional[APIError]:
        """
        Create a new embedding model.

        Args:
            embedding_model_request (EmbeddingModelRequest): Embedding model request object
        """
        with self._transaction():
            # Define embedding model
            embedding_model = EmbeddingModel(
                name=embedding_model_request.name,
                provider=embedding_model_request.provider,
                model_type=embedding_model_request.model_type,
                api_key=embedding_model_request.api_key,
                base_url=embedding_model_request.base_url,
                dimensions=embedding_model_request.dimensions,
                max_input_length=embedding_model_request.max_input_length,
                batch_size=embedding_model_request.batch_size,
                is_active=embedding_model_request.is_active,
            )

            # Create embedding model
            err = self._embedding_model_repo.create_embedding_model(embedding_model=embedding_model)

        return err if err else None

    def update_embedding_model(
        self, embedding_model_id: str, embedding_model_request: EmbeddingModelRequest
    ) -> Optional[APIError]:
        """
        Update an embedding model.

        Args:
            embedding_model_id (str): Embedding model id
            embedding_model_request (EmbeddingModelRequest): Embedding model request object
        """
        with self._transaction():
            # Define to-be-updated embedding model
            embedding_model = embedding_model_request.model_dump(exclude_unset=True)

            # Update embedding model
            err = self._embedding_model_repo.update_embedding_model(
                embedding_model_id=embedding_model_id, embedding_model=embedding_model
            )

        return err if err else None

    def delete_embedding_model(self, embedding_model_id: str) -> Optional[APIError]:
        """
        Delete an embedding model.

        Args:
            embedding_model_id (str): Embedding model id
        """
        with self._transaction():
            # Delete embedding model
            err = self._embedding_model_repo.delete_embedding_model(
                embedding_model_id=embedding_model_id
            )

        return err if err else None
