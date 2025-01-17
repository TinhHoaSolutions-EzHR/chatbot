import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import requests
from sqlalchemy.orm import Session

from app.models import UserSetting
from app.models.user import User
from app.models.user import UserRole
from app.models.user import UserSettingsRequest
from app.repositories.user import UserRepository
from app.repositories.user import UserSettingRepository
from app.services.base import BaseService
from app.settings import Constants
from app.settings import Secrets
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger


logger = get_logger(__name__)


class UserService(BaseService):
    """
    Service class for handling user-related operations such as retrieving user information
    from Google OAuth, fetching users by email, and creating users.
    """

    def __init__(self, db_session: Session):
        """
        Initializes the UserService with a database session.

        Args:
            db_session (Session): The SQLAlchemy database session.
        """
        super().__init__(db_session=db_session)
        self._user_repo = UserRepository(db_session=db_session)

    def get_user_from_google_oauth(
        self, code: str
    ) -> Tuple[Optional[Dict[str, Any]], Optional[APIError]]:
        """
        Retrieves user information from Google OAuth using the provided authorization code.

        Args:
            code (str): The authorization code from Google OAuth.

        Returns:
            Tuple[Optional[Dict[str, Any]], Optional[APIError]]: User information and APIError object if any error.
        """
        data = {
            "code": code,
            "client_id": Constants.GOOGLE_CLIENT_ID,
            "client_secret": Secrets.GOOGLE_CLIENT_SECRET,
            "redirect_uri": Constants.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        try:
            # Get the access token
            token_response = requests.post(Constants.GOOGLE_TOKEN_URL, data=data)
            access_token = token_response.json().get("access_token")

            # Get the user info
            user_info_response = requests.get(
                Constants.GOOGLE_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"}
            )

            return user_info_response.json(), None
        except Exception as e:
            logger.error(f"Error retrieving user information from Google OAuth: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_user_by_email(self, email: str) -> Tuple[Optional[User], Optional[APIError]]:
        """
        Retrieves a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            Tuple[Optional[User], Optional[APIError]]: A tuple containing the user object (if found) and an API error (if any).
        """
        return self._user_repo.get_user_by_email(email=email)

    def create_user(
        self, user_oauth_data: Dict[str, Any]
    ) -> Tuple[Optional[User], Optional[APIError]]:
        """
        Creates an user using data retrieved from Google OAuth.

        Args:
            user_oauth_data (Dict[str, Any]): A dictionary containing user information from Google OAuth.

        Returns:
            Tuple[Optional[User], Optional[APIError]]: A tuple containing the created user object and an API error (if any).
        """
        with self._transaction():
            # Define to-be-created user
            user = User(
                email=user_oauth_data.get("email"),
                name=user_oauth_data.get("name"),
                avatar=user_oauth_data.get("picture"),
                role=UserRole.ADMIN,
                is_oauth=True,
            )

            # Create user
            err = self._user_repo.create_user(user=user)
            if err:
                return None, err

        return user, None


class UserSettingService(BaseService):
    def __init__(self, db_session: Session):
        """
        User service class for handling user-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

        self._user_setting_repo = UserSettingRepository(db_session=db_session)

    def get_user_settings(
        self, user_settings_id: str
    ) -> Tuple[Optional[UserSetting], Optional[APIError]]:
        """
        Get user settings.

        Args:
            user_settings_id (str): User settings ID.

        Returns:
            Tuple[Optional[UserSetting], Optional[APIError]]: User settings and API error response.
        """
        user_settings, err = self._user_setting_repo.get_user_settings(
            user_settings_id=user_settings_id
        )
        if err:
            return None, err

        # Load recent agent IDs as a list
        if user_settings:
            if user_settings.recent_agent_ids:
                user_settings.recent_agent_ids = json.loads(user_settings.recent_agent_ids)
            else:
                user_settings.recent_agent_ids = []

        return user_settings, None

    def _handle_recent_agents(
        self, recent_agent_ids: Optional[List[str]], current_agent_id: str
    ) -> List[str]:
        """
        Handle recent agents.

        Args:
            recent_agent_ids (Optional[List[str]]): List of recent agent IDs
            current_agent_id (str): Current agent ID

        Returns:
            List[str]: Updated list of recent agent IDs
        """
        recent_agent_ids = [
            agent_id for agent_id in recent_agent_ids if agent_id != current_agent_id
        ]

        # Add current agent ID to the top of the list (mark as most recent)
        logger.info(f"Adding current agent ID to the top of the list: {current_agent_id}")
        recent_agent_ids.insert(0, current_agent_id)

        # We only keep the most recent agents
        recent_agent_ids = recent_agent_ids[: Constants.MAX_RECENT_AGENTS]
        logger.info("Updated recent agent IDs", extra={"recent_agent_ids": recent_agent_ids})

        return recent_agent_ids

    def create_user_settings(
        self, user_id: str
    ) -> Tuple[Optional[UserSetting], Optional[APIError]]:
        """
        Create user settings.

        Args:
            user_id (str): User ID.

        Returns:
            Tuple[Optional[UserSetting], Optional[APIError]]: User setting object and API error response.
        """
        with self._transaction():
            # Define to-be-created user settings
            user_settings = UserSetting(id=user_id)

            # Create user settings
            return self._user_setting_repo.create_user_settings(user_settings=user_settings)

    def update_user_settings(
        self, user_settings_id: str, user_settings_request: UserSettingsRequest
    ) -> Optional[APIError]:
        """
        Update user settings.

        Args:
            user_settings_id (str): User settings ID.
            user_settings_request (UserSettingsRequest): User setting request object.

        Returns:
            Optional[APIError]: API error response.
        """
        with self._transaction():
            # Define to-be-updated user settings
            user_settings = user_settings_request.model_dump(exclude_unset=True)

            # Fetch existing user setting
            existing_user_settings, err = self._user_setting_repo.get_user_settings(
                user_settings_id=user_settings_id
            )
            if err:
                return err

            # Handle recent agents
            if user_settings.get("current_agent_id"):
                recent_agent_ids = (
                    json.loads(existing_user_settings.recent_agent_ids)
                    if existing_user_settings.recent_agent_ids
                    else []
                )

                # Update recent agents
                current_agent_id = str(user_settings["current_agent_id"])
                recent_agent_ids = self._handle_recent_agents(
                    recent_agent_ids=recent_agent_ids, current_agent_id=current_agent_id
                )
                user_settings["recent_agent_ids"] = json.dumps(recent_agent_ids)

                # Remove the field from the request
                user_settings.pop("current_agent_id")

            # Update user settings
            err = self._user_setting_repo.update_user_settings(
                user_settings_id=user_settings_id, user_settings=user_settings
            )

        return err if err else None
