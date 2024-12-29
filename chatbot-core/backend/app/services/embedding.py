from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import EmbeddingProvider
from app.models.embedding import EmbeddingProviderRequest
from app.repositories.embedding import EmbeddingProviderRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.helpers import get_logger
from app.utils.llm.helpers import handle_current_embedding_model

logger = get_logger(__name__)


class EmbeddingProviderService(BaseService):
    def __init__(self, db_session: Session):
        """
        Embedding provider service class for handling embedding provider-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._embedding_provider_repo = EmbeddingProviderRepository(db_session=db_session)

    def get_embedding_providers(self) -> Tuple[List[EmbeddingProvider], Optional[APIError]]:
        """
        Get all embedding providers.

        Returns:
            Tuple[List[EmbeddingProvider], Optional[APIError]]: List of embedding provider objects and APIError object if any error.
        """
        return self._embedding_provider_repo.get_embedding_providers()

    def get_embedding_provider(
        self, embedding_provider_id: str
    ) -> Tuple[Optional[EmbeddingProvider], Optional[APIError]]:
        """
        Get an embedding provider by id.

        Args:
            embedding_provider_id (str): Embedding provider id.

        Returns:
            Tuple[Optional[EmbeddingProvider], Optional[APIError]]: Embedding provider object and APIError object if any error.
        """
        return self._embedding_provider_repo.get_embedding_provider(
            embedding_provider_id=embedding_provider_id
        )

    def update_embedding_provider(
        self, embedding_provider_id: str, embedding_provider_request: EmbeddingProviderRequest
    ) -> Optional[APIError]:
        """
        Update an embedding provider.

        Args:
            embedding_provider_id (str): Embedding provider id
            embedding_provider_request (EmbeddingProviderRequest): Embedding provider request object
        """
        # Get existing embedding provider
        existing_embedding_provider, err = self._embedding_provider_repo.get_embedding_provider(
            embedding_provider_id=embedding_provider_id
        )
        if err:
            return err

        with self._transaction():
            # Define to-be-updated embedding provider
            embedding_provider = embedding_provider_request.model_dump(exclude_unset=True)

            # Set the current embedding model
            if embedding_provider.get("current_model") and embedding_provider.get("name"):
                # Update settings
                handle_current_embedding_model(
                    embedding_model_name=embedding_provider["current_model"],
                    embedding_type=embedding_provider["name"],
                    batch_size=embedding_provider.get("embed_batch_size")
                    or existing_embedding_provider.embed_batch_size,
                    dimensions=embedding_provider.get("dimensions")
                    or existing_embedding_provider.dimensions,
                    api_key=embedding_provider.get("api_key")
                    or existing_embedding_provider.api_key,
                )

            # Update embedding provider
            err = self._embedding_provider_repo.update_embedding_provider(
                embedding_provider_id=embedding_provider_id, embedding_provider=embedding_provider
            )

        return err if err else None
