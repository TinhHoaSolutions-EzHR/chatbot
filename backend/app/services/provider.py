import json
from typing import List
from typing import Optional
from typing import Tuple

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from app.models import EmbeddingProvider
from app.models import LLMProvider
from app.models.provider import EmbeddingProviderRequest
from app.models.provider import LLMProviderRequest
from app.repositories.provider import ProviderRepository
from app.services.base import BaseService
from app.settings import Secrets
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
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
        embedding_providers, err = self._provider_repo.get_embedding_providers()
        if err:
            return [], err

        # Parse the models field
        for embedding_provider in embedding_providers:
            embedding_provider.models = (
                json.loads(embedding_provider.models) if embedding_provider.models else []
            )

        return embedding_providers, None

    def get_llm_providers(self) -> Tuple[List[LLMProvider], Optional[APIError]]:
        """
        Get all LLM providers.

        Returns:
            Tuple[List[LLMProvider], Optional[APIError]]: List of LLM provider objects and APIError object if any error.
        """
        llm_providers, err = self._provider_repo.get_llm_providers()
        if err:
            return [], err

        # Parse the models field
        for llm_provider in llm_providers:
            llm_provider.models = json.loads(llm_provider.models) if llm_provider.models else []

        return llm_providers, None

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
        embedding_provider, err = self._provider_repo.get_embedding_provider(
            embedding_provider_id=embedding_provider_id
        )
        if err:
            return None, err

        # Parse the models field
        embedding_provider.models = (
            json.loads(embedding_provider.models) if embedding_provider.models else []
        )

        return embedding_provider, None

    def get_llm_provider(self, llm_provider_id: str) -> Tuple[LLMProvider, Optional[APIError]]:
        """
        Get LLM provider by ID.

        Args:
            llm_provider_id (str): The LLM provider ID.

        Returns:
            Tuple[LLMProvider, Optional[APIError]]: LLM provider object and APIError object if any error.
        """
        # Get LLM provider
        llm_provider, err = self._provider_repo.get_llm_provider(llm_provider_id=llm_provider_id)
        if err:
            return None, err

        # Parse the models field
        llm_provider.models = json.loads(llm_provider.models) if llm_provider.models else []

        return llm_provider, None

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

            # Check whether the provider is changed (we do not allow changing the provider type)
            if embedding_provider.get("name") != existing_embedding_provider.name:
                return APIError(kind=ErrorCodesMappingNumber.PROVIDER_TYPE_CHANGE_NOT_ALLOWED.value)

            # Parse the models field
            if embedding_provider.get("models"):
                embedding_provider["models"] = json.dumps(embedding_provider["models"])

            # Handle current api key
            api_key = None
            fernet = Fernet(Secrets.FERMENT_API_KEY)
            if embedding_provider.get("api_key"):
                api_key = embedding_provider["api_key"]

                # Encrypt the new api key
                encryption_result = fernet.encrypt(embedding_provider["api_key"].encode())
                embedding_provider["api_key"] = encryption_result
            else:
                # Use the existing api key
                api_key = fernet.decrypt(existing_embedding_provider.api_key).decode()

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
            llm_provider = llm_provider_request.model_dump(exclude_unset=True)

            # Check whether the provider is changed (we do not allow changing the provider type)
            if llm_provider.get("name") != existing_llm_provider.name:
                return APIError(kind=ErrorCodesMappingNumber.PROVIDER_TYPE_CHANGE_NOT_ALLOWED.value)

            # Parse the models field
            if llm_provider.get("models"):
                llm_provider["models"] = json.dumps(llm_provider["models"])

            # Handle current api key
            api_key = None
            fernet = Fernet(Secrets.FERMENT_API_KEY)
            if llm_provider.get("api_key"):
                api_key = llm_provider["api_key"]

                # Encrypt the new api key
                encryption_result = fernet.encrypt(llm_provider["api_key"].encode())
                llm_provider["api_key"] = encryption_result
            else:
                # Use the existing api key
                api_key = fernet.decrypt(existing_llm_provider.api_key).decode()

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
