from typing import Optional

from sqlalchemy.orm import Session

from app.models import User
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class UserRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        User repository class for handling user-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def update_user(self, user_id: str, user: User) -> Optional[APIError]:
        """
        Update user.

        Args:
            user (User): User object

        Returns:
            Optional[APIError]: API error response
        """
        try:
            user = {key: value for key, value in user.__dict__.items() if not key.startswith("_")}
            self._db_session.query(User).filter(User.id == user_id).update(user)
            return None
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
