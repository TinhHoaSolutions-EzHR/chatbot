from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import EmbeddingProvider
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class EmbeddingProviderRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Embedding provider repository class for handling embedding provider-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_embedding_providers(self) -> Tuple[List[EmbeddingProvider], Optional[APIError]]:
        """
        Get all embedding providers.

        Returns:
            Tuple[List[EmbeddingProvider], Optional[APIError]]: List of embedding provider objects and APIError object if any error.
        """
        try:
            embedding_providers = self._db_session.query(EmbeddingProvider).all()
            return embedding_providers, None
        except Exception as e:
            logger.error(f"Error getting embedding providers: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_embedding_provider(
        self, embedding_provider_id: str
    ) -> Tuple[Optional[EmbeddingProvider], Optional[APIError]]:
        """
        Get an embedding provider by ID.

        Args:
            embedding_provider_id (str): Embedding provider id

        Returns:
            Tuple[Optional[EmbeddingProvider], Optional[APIError]]: embedding provider object and APIError object if any error
        """
        try:
            embedding_provider = (
                self._db_session.query(EmbeddingProvider)
                .filter(EmbeddingProvider.id == embedding_provider_id)
                .first()
            )
            return embedding_provider, None
        except Exception as e:
            logger.error(f"Error getting embedding provider: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_embedding_provider(
        self, embedding_provider: EmbeddingProvider
    ) -> Optional[APIError]:
        """
        Create an embedding provider.

        Args:
            embedding_provider (EmbeddingProvider): embedding provider object.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        try:
            self._db_session.add(embedding_provider)
            return None
        except Exception as e:
            logger.error(f"Error creating embedding provider: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_embedding_provider(
        self, embedding_provider_id: str, embedding_provider: Dict[str, Any]
    ) -> Optional[APIError]:
        """
        Update an embedding provider.

        Args:
            embedding_provider_id (str): embedding provider id.
            embedding_provider (Dict[str, Any]): embedding provider data.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        try:
            self._db_session.query(EmbeddingProvider).filter(
                EmbeddingProvider.id == embedding_provider_id
            ).update(embedding_provider)
            return None
        except Exception as e:
            logger.error(f"Error updating embedding provider: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_embedding_provider(self, embedding_provider_id: str) -> Optional[APIError]:
        """
        Delete an embedding provider.

        Args:
            embedding_provider_id (str): embedding provider id.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        try:
            self._db_session.query(EmbeddingProvider).filter(
                EmbeddingProvider.id == embedding_provider_id
            ).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting embedding provider: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
