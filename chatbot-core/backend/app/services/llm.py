from typing import List
from typing import Optional
from typing import Tuple

from llama_index.core import Settings
from sqlalchemy.orm import Session

from app.models import LLMProvider
from app.models.llm import LLMProviderRequest
from app.repositories.llm import LLMProviderRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.helpers import get_logger
from app.utils.llm.helpers import handle_current_llm_model


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
            Tuple[List[LLMProvider], Optional[APIError]]: List of LLM provider objects and APIError object if any error.
        """
        return self._llm_provider_repo.get_llm_providers()

    def get_llm_provider(self, llm_provider_id: str) -> Tuple[LLMProvider, Optional[APIError]]:
        """
        Get LLM provider by ID.

        Args:
            llm_provider_id (str): The LLM provider ID.

        Returns:
            Tuple[LLMProvider, Optional[APIError]]: LLM provider object and APIError object if any error.
        """
        # Get LLM provider
        return self._llm_provider_repo.get_llm_provider(llm_provider_id=llm_provider_id)

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
        existing_llm_provider, err = self._llm_provider_repo.get_llm_provider(
            llm_provider_id=llm_provider_id
        )
        if err:
            return err

        with self._transaction():
            # Define to-be-updated LLM provider
            llm_provider = llm_provider_request.model_dump(exclude_unset=True, exclude_none=True)

            # Set the current LLM model
            if llm_provider.get("current_model") and llm_provider.get("name"):
                Settings.llm = handle_current_llm_model(
                    llm_model_name=llm_provider["current_model"],
                    llm_provider_type=llm_provider["name"],
                    temperature=llm_provider.get("temperature")
                    or existing_llm_provider.temperature,
                    api_key=llm_provider.get("api_key") or existing_llm_provider.api_key,
                    logger=logger,
                )

            # Update LLM provider
            err = self._llm_provider_repo.update_llm_provider(
                llm_provider_id=llm_provider_id, llm_provider=llm_provider
            )

        return err if err else None
