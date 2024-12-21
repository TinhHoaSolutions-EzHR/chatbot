from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import Prompt
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class PromptRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Prompt repository class for handling prompt-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_prompt(self, prompt_id: str) -> Tuple[Prompt, Optional[APIError]]:
        """
        Get a prompt by prompt id.

        Args:
            prompt_id(str): Prompt id

        Returns:
            Tuple[Prompt, Optional[APIError]]: Prompt object and APIError object if any error
        """
        try:
            prompt = self._db_session.query(Prompt).filter(Prompt.id == prompt_id).first()
            return prompt, None
        except Exception as e:
            logger.error(f"Error getting prompt: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_prompt(self, prompt: Prompt) -> Optional[APIError]:
        """
        Create a prompt.

        Args:
            prompt(Prompt): Prompt object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(prompt)
            return None
        except Exception as e:
            logger.error(f"Error creating prompt: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_prompt(self, prompt_id: str, prompt: Dict[str, Any]) -> Optional[APIError]:
        """
        Update a prompt.

        Args:
            prompt_id(str): Prompt id
            prompt(Dict[str, Any]): Prompt object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(Prompt).filter(Prompt.id == prompt_id).update(prompt)
            return None
        except Exception as e:
            logger.error(f"Error updating prompt: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
