from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from app.models import User
from app.models.user import UserSettingRequest
from app.repositories.user import UserRepository
from app.services.base import BaseService
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

        self._user_repo = UserRepository(db_session=db_session)

    def _handle_recent_agents(
        self, recent_agent_ids: Optional[List[str]], current_agent_id: str
    ) -> Optional[List[str]]:
        """
        Handle recent agents.

        Args:
            recent_agent_ids (Optional[List[str]]): List of recent agent IDs
            current_agent_id (str): Current agent ID

        Returns:
            Optional[List[str]]: List of recent agent IDs
        """
        if not recent_agent_ids:
            recent_agent_ids = []
        else:
            recent_agent_ids = [agent_id for agent_id in recent_agent_ids if agent_id != current_agent_id]

        # Add the current agent ID to the beginning of the list
        recent_agent_ids.insert(0, current_agent_id)

        # Limit the number of recent agents to 5
        recent_agent_ids = recent_agent_ids[:5]

        return recent_agent_ids

    def update_user_settings(self, user: User, user_setting_request: UserSettingRequest) -> Optional[APIError]:
        """
        Update user settings.

        Args:
            user (User): User object
            user_setting_request (UserSettingRequest): User setting request object

        Returns:
            Optional[APIError]: API error response
        """
        with self._transaction():
            # Handle update recent agents
            recent_agent_ids = user.recent_agent_ids
            if user_setting_request.current_agent_id:
                current_agent_id = user_setting_request.current_agent_id
                recent_agent_ids = self._handle_recent_agents(
                    recent_agent_ids=recent_agent_ids, current_agent_id=current_agent_id
                )

                # Update user recent agents
                user.recent_agent_ids = recent_agent_ids

            # Update other user settings
            user.auto_scroll = user_setting_request.auto_scroll

            err = self._user_repo.update_user(user_id=user.id, user=user)

        return err if err else None
