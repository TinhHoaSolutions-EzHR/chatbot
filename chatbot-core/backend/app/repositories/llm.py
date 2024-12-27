from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import LLMModel
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class LLMModelRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        LLM model repository class for handling llm model-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_llm_models(self) -> Tuple[List[LLMModel], Optional[APIError]]:
        """
        Get all llm models.

        Returns:
            Tuple[List[LLMModel], Optional[APIError]]: List of llm model objects and APIError object if any error
        """
        try:
            llm_models = self._db_session.query(LLMModel).all()
            return llm_models, None
        except Exception as e:
            logger.error(f"Error getting llm models: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_llm_model(self, llm_model_id: str) -> Tuple[Optional[LLMModel], Optional[APIError]]:
        """
        Get an llm model by id.

        Args:
            llm_model_id (str): LLM model id

        Returns:
            Tuple[Optional[LLMModel], Optional[APIError]]: LLM model object and APIError object if any error
        """
        try:
            llm_model = self._db_session.query(LLMModel).filter(LLMModel.id == llm_model_id).first()
            return llm_model, None
        except Exception as e:
            logger.error(f"Error getting llm model: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_llm_model(self, llm_model: LLMModel) -> Optional[APIError]:
        """
        Create an llm model.

        Args:
            llm_model (LLMModel): LLM model object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(llm_model)
            return None
        except Exception as e:
            logger.error(f"Error creating llm model: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_llm_model(self, llm_model_id: str, llm_model: Dict[str, Any]) -> Optional[APIError]:
        """
        Update an llm model.

        Args:
            llm_model_id (str): LLM model id
            llm_model (Dict[str, Any]): LLM model data

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(LLMModel).filter(LLMModel.id == llm_model_id).update(llm_model)
            return None
        except Exception as e:
            logger.error(f"Error updating llm model: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_llm_model(self, llm_model_id: str) -> Optional[APIError]:
        """
        Delete an llm model.

        Args:
            llm_model_id (str): LLM model id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(LLMModel).filter(LLMModel.id == llm_model_id).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting llm model: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
