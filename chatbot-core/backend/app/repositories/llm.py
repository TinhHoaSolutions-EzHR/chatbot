from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import LLMProvider
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class LLMProviderRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        LLM provider repository class for handling LLM provider-related database operations.

        Args:
            db_session (Session): Database session.
        """
        super().__init__(db_session=db_session)

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
            Tuple[LLMProvider, Optional[APIError]]: LLM provider object and APIError object if any error
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

    def create_llm_provider(self, llm_provider: LLMProvider) -> Optional[APIError]:
        """
        Create LLM provider.

        Args:
            llm_provider (LLMProvider): The LLM provider object.

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(llm_provider)
            return None
        except Exception as e:
            logger.error(f"Error creating LLM provider: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_llm_provider(
        self, llm_provider_id: str, llm_provider: Dict[str, Any]
    ) -> Optional[APIError]:
        """
        Update LLM provider.

        Args:
            llm_provider_id (str): The LLM provider ID.
            llm_provider (LLMProvider): The LLM provider object.

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(LLMProvider).filter(LLMProvider.id == llm_provider_id).update(
                llm_provider
            )
            return None
        except Exception as e:
            logger.error(f"Error updating LLM provider: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_llm_provider(self, llm_provider_id: str) -> Optional[APIError]:
        """
        Delete LLM provider.

        Args:
            llm_provider_id (str): The LLM provider ID.

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(LLMProvider).filter(LLMProvider.id == llm_provider_id).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting LLM provider: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
