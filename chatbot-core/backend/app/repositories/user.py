from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.models import User, UserSetting
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

# Initialize logger
logger = get_logger(__name__)


class UserRepository(BaseRepository):
    """
    UserRepository handles database operations related to the User model.
    """

    def __init__(self, db_session: Session):
        """
        Initializes the UserRepository with a database session.

        Args:
            db_session (Session): The SQLAlchemy database session.
        """
        super().__init__(db_session=db_session)

    def get_user_by_email(self, email: str) -> Tuple[Optional[User], Optional[APIError]]:
        """
        Retrieves a user from the database by email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            Tuple[Optional[User], Optional[APIError]]: A tuple containing the User object
            (if found) and an optional APIError object.
        """
        try:
            user = self._db_session.query(User).filter(User.email == email).first()
            return user, None
        except Exception as error:
            logger.error(f"Error retrieving user by email: {error}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_user(self, user: User) -> Optional[APIError]:
        """
        Creates a new user in the database.

        Args:
            user (User): The User object to create.

        Returns:
            Optional[APIError]: An APIError object if an error occurs, otherwise None.
        """
        try:
            self._db_session.add(user)
            return None
        except Exception as error:
            logger.error(f"Error creating user: {error}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)


class UserSettingRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        User setting repository class for handling user setting-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_user_settings(self, user_id: str) -> Tuple[UserSetting, Optional[APIError]]:
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
            logger.error(f"Error getting user settings: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_user_settings(self, user_id: str, user_settings: UserSetting) -> Optional[APIError]:
        """
        Update user settings.

        Args:
            user_setting (UserSetting): User setting object

        Returns:
            Optional[APIError]: API error response
        """
        try:
            self._db_session.query(UserSetting).filter(UserSetting.id == user_id).update(
                user_settings
            )
            return None
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
