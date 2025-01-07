from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import EmbeddingProvider
from app.models import LLMProvider
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class ProviderRepository(BaseRepository):
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
            # Check if the embedding provider exists
            embedding_provider_exists = (
                self._db_session.query(EmbeddingProvider)
                .filter(EmbeddingProvider.id == embedding_provider_id)
                .first()
            )
            if not embedding_provider_exists:
                return APIError(kind=ErrorCodesMappingNumber.EMBEDDING_PROVIDER_NOT_FOUND.value)

            # Update the embedding provider
            self._db_session.query(EmbeddingProvider).filter(
                EmbeddingProvider.id == embedding_provider_id
            ).update(embedding_provider)
            return None
        except Exception as e:
            logger.error(f"Error updating embedding provider: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_llm_providers(self) -> Tuple[List[LLMProvider], Optional[APIError]]:
        """
        Get all LLM providers.

        Returns:
            Tuple[List[LLMProvider], Optional[APIError]]: List of LLM provider objects and APIError object if any error.
        """
        try:
            llm_providers = self._db_session.query(LLMProvider).all()
            return llm_providers, None
        except Exception as e:
            logger.error(f"Error getting LLM providers: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_llm_provider(self, llm_provider_id: str) -> Tuple[LLMProvider, Optional[APIError]]:
        """
        Get LLM provider by ID.

        Args:
            llm_provider_id (str): The LLM provider ID.

        Returns:
            Tuple[LLMProvider, Optional[APIError]]: LLM provider object and APIError object if any error.
        """
        try:
            llm_provider = (
                self._db_session.query(LLMProvider)
                .filter(LLMProvider.id == llm_provider_id)
                .first()
            )
            return llm_provider, None
        except Exception as e:
            logger.error(f"Error getting LLM provider: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_llm_provider(
        self, llm_provider_id: str, llm_provider: Dict[str, Any]
    ) -> Optional[APIError]:
        """
        Update LLM provider.

        Args:
            llm_provider_id (str): The LLM provider ID.
            llm_provider (LLMProvider): The LLM provider object.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        try:
            # Check if the LLM provider exists
            llm_provider_exists = (
                self._db_session.query(LLMProvider)
                .filter(LLMProvider.id == llm_provider_id)
                .first()
            )
            if not llm_provider_exists:
                return APIError(kind=ErrorCodesMappingNumber.LLM_PROVIDER_NOT_FOUND.value)

            # Update the LLM provider
            self._db_session.query(LLMProvider).filter(LLMProvider.id == llm_provider_id).update(
                llm_provider
            )
            return None
        except Exception as e:
            logger.error(f"Error updating LLM provider: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
