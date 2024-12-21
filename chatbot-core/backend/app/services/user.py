import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user import UserSettingRequest
from app.repositories.user import UserSettingRepository
from app.services.base import BaseService
from app.settings import Constants
from app.utils.api.api_response import APIError
from app.utils.api.helpers import get_logger


logger = get_logger(__name__)


class UserService(BaseService):
    def __init__(self, db_session: Session):
        """
        User service class for handling user-related operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

        self._user_setting_repo = UserSettingRepository(db_session=db_session)

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

    def update_user_settings(
        self, user: User, user_setting_request: UserSettingRequest
    ) -> Optional[APIError]:
        """
        Update user settings.

        Args:
            user (User): User object
            user_setting_request (UserSettingRequest): User setting request object

        Returns:
            Optional[APIError]: API error response
        """
        with self._transaction():
            user_settings: Dict[str, Any] = user_setting_request.model_dump(exclude_unset=True)

            # Fetch existing user setting
            existing_user_settings, err = self._user_setting_repo.get_user_settings(user_id=user.id)
            if err:
                return err

            # Handle recent agents
            if user_settings.get("current_agent_id"):
                recent_agent_ids = (
                    json.loads(existing_user_settings.recent_agent_ids)
                    if existing_user_settings.recent_agent_ids
                    else []
                )
                logger.info(f"Current recent agent IDs: {recent_agent_ids}")

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
                user_id=user.id, user_settings=user_settings
            )

        return err if err else None
