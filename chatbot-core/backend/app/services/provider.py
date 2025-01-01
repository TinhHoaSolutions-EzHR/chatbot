from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import EmbeddingProvider
from app.models import LLMProvider
from app.models.provider import EmbeddingProviderRequest
from app.models.provider import LLMProviderRequest
from app.repositories.provider import ProviderRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.encryption import SecretKeyManager
from app.utils.api.helpers import get_logger
from app.utils.llm.helpers import handle_current_embedding_model
from app.utils.llm.helpers import handle_current_llm_model

logger = get_logger(__name__)


class ProviderService(BaseService):
    def __init__(self, db_session: Session):
        """
        Embedding provider service class for handling embedding provider-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._provider_repo = ProviderRepository(db_session=db_session)

    def get_embedding_providers(self) -> Tuple[List[EmbeddingProvider], Optional[APIError]]:
        """
        Get all embedding providers.

        Returns:
            Tuple[List[EmbeddingProvider], Optional[APIError]]: List of embedding provider objects and APIError object if any error.
        """
        return self._provider_repo.get_embedding_providers()

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
        return self._provider_repo.get_embedding_provider(
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
        existing_embedding_provider, err = self._provider_repo.get_embedding_provider(
            embedding_provider_id=embedding_provider_id
        )
        if err:
            return err

        with self._transaction():
            # Define to-be-updated embedding provider
            embedding_provider = embedding_provider_request.model_dump(exclude_unset=True)

            # Handle current api key
            api_key = None
            if embedding_provider.get("api_key"):
                # Encrypt the new api key
                api_key = embedding_provider["api_key"]
                secret_key_manager = SecretKeyManager(db_session=self._db_session)
                encryption_result = secret_key_manager.encrypt_key(embedding_provider["api_key"])
                embedding_provider["api_key"] = encryption_result
            else:
                # Use the existing api key
                api_key = existing_embedding_provider.api_key

            # Set the current embedding model
            if embedding_provider.get("current_model"):
                # Update settings
                handle_current_embedding_model(
                    embedding_model_name=embedding_provider["current_model"],
                    provider_type=existing_embedding_provider.name,
                    batch_size=embedding_provider.get("embed_batch_size")
                    or existing_embedding_provider.embed_batch_size,
                    dimensions=embedding_provider.get("dimensions")
                    or existing_embedding_provider.dimensions,
                    api_key=api_key,
                )

            # Update embedding provider
            err = self._provider_repo.update_embedding_provider(
                embedding_provider_id=embedding_provider_id, embedding_provider=embedding_provider
            )

        return err if err else None

    def get_llm_providers(self) -> Tuple[List[LLMProvider], Optional[APIError]]:
        """
        Get all LLM providers.

        Returns:
            Tuple[List[LLMProvider], Optional[APIError]]: List of LLM provider objects and APIError object if any error.
        """
        return self._provider_repo.get_llm_providers()

    def get_llm_provider(self, llm_provider_id: str) -> Tuple[LLMProvider, Optional[APIError]]:
        """
        Get LLM provider by ID.

        Args:
            llm_provider_id (str): The LLM provider ID.

        Returns:
            Tuple[LLMProvider, Optional[APIError]]: LLM provider object and APIError object if any error.
        """
        # Get LLM provider
        return self._provider_repo.get_llm_provider(llm_provider_id=llm_provider_id)

    def update_llm_provider(
        self, llm_provider_id: str, llm_provider_request: LLMProviderRequest
    ) -> Optional[APIError]:
        """
        Update LLM provider.

        Args:
            llm_provider_id (str): The LLM provider ID.
            llm_provider_request (LLMProviderRequest): The LLM provider request.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        # Get existing LLM provider
        existing_llm_provider, err = self._provider_repo.get_llm_provider(
            llm_provider_id=llm_provider_id
        )
        if err:
            return err

        with self._transaction():
            # Define to-be-updated LLM provider
            llm_provider = llm_provider_request.model_dump(exclude_unset=True, exclude_none=True)

            # Handle current api key
            api_key = None
            if llm_provider.get("api_key"):
                # Encrypt the new api key
                api_key = llm_provider["api_key"]
                secret_key_manager = SecretKeyManager(db_session=self._db_session)
                encryption_result = secret_key_manager.encrypt_key(llm_provider["api_key"])
                llm_provider["api_key"] = encryption_result
            else:
                # Use the existing api key
                api_key = existing_llm_provider.api_key

            # Set the current LLM model
            if llm_provider.get("current_model"):
                handle_current_llm_model(
                    llm_model_name=llm_provider["current_model"],
                    provider_type=existing_llm_provider.name,
                    temperature=llm_provider.get("temperature")
                    or existing_llm_provider.temperature,
                    api_key=api_key,
                    logger=logger,
                )

            # Update LLM provider
            err = self._provider_repo.update_llm_provider(
                llm_provider_id=llm_provider_id, llm_provider=llm_provider
            )

        return err if err else None
