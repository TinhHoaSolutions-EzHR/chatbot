from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import LLMModel
from app.models.llm import LLMModelRequest
from app.repositories.llm import LLMModelRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class LLMModelService(BaseService):
    def __init__(self, db_session: Session):
        """
        LLM model service class for handling LLM model-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._llm_model_repo = LLMModelRepository(db_session=db_session)

    def get_llm_models(self) -> Tuple[List[LLMModel], Optional[APIError]]:
        """
        Get all LLM models.

        Returns:
            Tuple[List[LLMModel], Optional[APIError]]: List of LLM model objects and APIError object if any error
        """
        return self._llm_model_repo.get_llm_models()

    def get_llm_model(self, llm_model_id: str) -> Tuple[Optional[LLMModel], Optional[APIError]]:
        """
        Get an LLM model by id.

        Args:
            llm_model_id (str): LLM model id

        Returns:
            Tuple[Optional[LLMModel], Optional[APIError]]: LLM model object and APIError object if any error
        """
        return self._llm_model_repo.get_llm_model(llm_model_id=llm_model_id)

    def create_llm_model(self, llm_model_request: LLMModelRequest) -> Optional[APIError]:
        """
        Create a new LLM model.

        Args:
            llm_model_request (LLMModelRequest): LLM model request object
        """
        with self._transaction():
            # Define LLM model
            llm_model = LLMModel(
                name=llm_model_request.name,
                provider=llm_model_request.provider,
                model_type=llm_model_request.model_type,
                api_key=llm_model_request.api_key,
                base_url=llm_model_request.base_url,
                context_length=llm_model_request.context_length,
                max_tokens=llm_model_request.max_tokens,
                temperature=llm_model_request.temperature,
                top_p=llm_model_request.top_p,
                frequency_penalty=llm_model_request.frequency_penalty,
                presence_penalty=llm_model_request.presence_penalty,
                is_active=llm_model_request.is_active,
            )

            # Create LLM model
            err = self._llm_model_repo.create_llm_model(llm_model=llm_model)

        return err if err else None

    def update_llm_model(
        self, llm_model_id: str, llm_model_request: LLMModelRequest
    ) -> Optional[APIError]:
        """
        Update an LLM model.

        Args:
            llm_model_id (str): LLM model id
            llm_model_request (LLMModelRequest): LLM model request object
        """
        with self._transaction():
            # Define to-be-updated LLM model
            llm_model = llm_model_request.model_dump(exclude_unset=True)

            # Update LLM model
            err = self._llm_model_repo.update_llm_model(
                llm_model_id=llm_model_id, llm_model=llm_model
            )

        return err if err else None

    def delete_llm_model(self, llm_model_id: str) -> Optional[APIError]:
        """
        Delete an LLM model.

        Args:
            llm_model_id (str): LLM model id
        """
        with self._transaction():
            # Delete LLM model
            err = self._llm_model_repo.delete_llm_model(llm_model_id=llm_model_id)

        return err if err else None
