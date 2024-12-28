import json
from typing import List
from typing import Optional
from typing import Tuple

from llama_index.core import Settings
from llama_index.llms.litellm import LiteLLM
from sqlalchemy.orm import Session

from app.models import LLMProvider
from app.models.llm import LLMProviderRequest
from app.repositories.llm import LLMProviderRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger


logger = get_logger(__name__)


class LLMProviderService(BaseService):
    def __init__(self, db_session: Session):
        """
        LLM provider service class for handling LLM provider-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._llm_provider_repo = LLMProviderRepository(db_session=db_session)

    def get_llm_providers(self) -> Tuple[List[LLMProvider], Optional[APIError]]:
        """
        Get all LLM providers.

        Returns:
            Tuple[List[LLMProvider], Optional[APIError]]: List of LLM provider objects and APIError object if any error
        """
        return self._llm_provider_repo.get_llm_providers()

    def get_llm_provider(self, llm_provider_id: str) -> Tuple[LLMProvider, Optional[APIError]]:
        """
        Get LLM provider by ID.

        Args:
            llm_provider_id (str): The LLM provider ID.

        Returns:
            Tuple[LLMProvider, Optional[APIError]]: LLM provider object and APIError object if any error
        """
        # Get LLM provider
        llm_provider, err = self._llm_provider_repo.get_llm_provider(
            llm_provider_id=llm_provider_id
        )
        if err:
            return None, err

        # Parse LLM's models and configurations to appropriate objects
        try:
            llm_provider.model_names = json.loads(llm_provider.model_names)
            llm_provider.model_config = json.loads(llm_provider.model_config)
        except Exception as e:
            logger.error(f"Error parsing LLM provider models and configurations: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return llm_provider, None

    def create_llm_provider(self, llm_provider_request: LLMProviderRequest) -> Optional[APIError]:
        """
        Create LLM provider.

        Args:
            llm_provider_request (LLMProviderRequest): The LLM provider request.

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Convert LLM's models and configurations to JSON strings
            llm_provider_request.model_names = json.dumps(llm_provider_request.model_names)
            llm_provider_request.model_config = json.dumps(llm_provider_request.model_config)

            # Define to-be-created LLM provider
            llm_provider = LLMProvider(**llm_provider_request.model_dump())

            # Create LLM provider
            err = self._llm_provider_repo.create_llm_provider(llm_provider=llm_provider)

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
            Optional[APIError]: APIError object if any error
        """
        # Get existing LLM provider
        existing_llm_provider, err = self._llm_provider_repo.get_llm_provider(
            llm_provider_id=llm_provider_id
        )
        if err:
            return err

        with self._transaction():
            # Define to-be-updated LLM provider
            llm_provider = llm_provider_request.model_dump(exclude_unset=True, exclude_none=True)

            # Convert LLM's models and configurations to JSON strings
            try:
                if llm_provider.get("model_names"):
                    llm_provider["model_names"] = json.dumps(llm_provider["model_names"])
                if llm_provider.get("model_config"):
                    llm_provider["model_config"] = json.dumps(llm_provider["model_config"])
            except (TypeError, ValueError) as e:
                return APIError(message=f"Invalid JSON data: {str(e)}")

            # Set the current LLM model
            if llm_provider.get("current_model"):
                Settings.llm = LiteLLM(
                    model=llm_provider.get("current_model") or existing_llm_provider.current_model,
                    api_key=llm_provider.get("api_key") or existing_llm_provider.api_key,
                    api_base=llm_provider.get("api_base") or existing_llm_provider.api_base,
                    temperature=llm_provider.get("temperature")
                    or existing_llm_provider.temperature,
                    model_config=llm_provider.get("model_config")
                    or existing_llm_provider.model_config,
                )

            # Update LLM provider
            err = self._llm_provider_repo.update_llm_provider(
                llm_provider_id=llm_provider_id, llm_provider=llm_provider
            )

        return err if err else None

    def delete_llm_provider(self, llm_provider_id: str) -> Optional[APIError]:
        """
        Delete LLM provider.

        Args:
            llm_provider_id (str): The LLM provider ID.

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Delete LLM provider
            err = self._llm_provider_repo.delete_llm_provider(llm_provider_id=llm_provider_id)

        return err if err else None
