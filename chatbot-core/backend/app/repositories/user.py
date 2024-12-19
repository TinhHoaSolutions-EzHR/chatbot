from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import User
from app.models import UserSetting
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

    def get_user(self, user_id: str) -> Tuple[User, Optional[APIError]]:
        """
        Get user by id.

        Args:
            user_id (str): User ID

        Returns:
            Tuple[User, Optional[APIError]]: User object and API error response
        """
        try:
            user = self._db_session.query(User).filter(User.id == user_id).first()
            return user, None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)


class UserSettingRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        User setting repository class for handling user setting-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_user_setting(self, user_id: str) -> Tuple[UserSetting, Optional[APIError]]:
        """
        Get user settings by user ID.

        Args:
            user_id (str): User ID

        Returns:
            Tuple[UserSetting, Optional[APIError]]: User setting object and API error response
        """
        try:
            user_setting = (
                self._db_session.query(UserSetting).filter(UserSetting.id == user_id).first()
            )
            return user_setting, None
        except Exception as e:
            logger.error(f"Error getting user setting: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_user_setting(self, user_id: str, user_setting: UserSetting) -> Optional[APIError]:
        """
        Update user settings.

        Args:
            user_setting (UserSetting): User setting object

        Returns:
            Optional[APIError]: API error response
        """
        try:
            user_setting = {
                key: value
                for key, value in user_setting.__dict__.items()
                if not key.startswith("_")
            }
            self._db_session.query(UserSetting).filter(UserSetting.id == user_id).update(
                user_setting
            )
            return None
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
