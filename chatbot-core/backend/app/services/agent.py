from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session

from app.models import Agent
from app.models.agent import AgentRequest
from app.repositories.agent import AgentRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class AgentService(BaseService):
    def __init__(self, db_session: Session):
        """
        Agent service class for handling agent-related operations.

        Args:
            db_session(Session): Database session
        """
        super().__init__(db_session)

        self._agent_repo = AgentRepository(db_session=db_session)

    def get_agents(self, user_id: str) -> Tuple[Optional[List[Agent]], Optional[APIError]]:
        """
        Get all agents of the user. Sort by display_priority.

        Args:
            user_id(str): User id

        Returns:
            Tuple[Optional[List[Agent]], Optional[APIError]]: List of agent objects and APIError object if any error
        """
        return self._agent_repo.get_agents(user_id=user_id)

    def get_agent(self, agent_id: str, user_id: str) -> Tuple[Optional[Agent], Optional[APIError]]:
        """
        Get an agent by id.

        Args:
            agent_id(str): Agent id
            user_id(str): User id

        Returns:
            Tuple[Optional[Agent], Optional[APIError]]: Agent object and APIError object if any error
        """
        return self._agent_repo.get_agent(agent_id=agent_id, user_id=user_id)

    def create_agent(self, agent_request: AgentRequest) -> Optional[APIError]:
        """
        Create a new agent.

        Args:
            agent_request(AgentRequest): Agent request object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define agent
            agent = Agent(
                name=agent_request.name,
                description=agent_request.description,
                agent_type=agent_request.agent_type,
                uploaded_image_id=agent_request.uploaded_image_id,
            )

            # Create agent
            err = self._agent_repo.create_agent(agent=agent)

        return err if err else None

    def update_agent(
        self, agent_id: str, agent_request: AgentRequest, user_id: str
    ) -> Optional[APIError]:
        """
        Update an agent.

        Args:
            agent_id(str): Agent id
            agent_request(AgentRequest): Agent request object
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define to-be-updated agent
            agent = agent_request.model_dump(exclude_unset=True)

            # Update agent
            err = self._agent_repo.update_agent(agent_id=agent_id, agent=agent, user_id=user_id)

        return err if err else None

    def delete_agent(self, agent_id: str, user_id: str) -> Optional[APIError]:
        """
        Delete an agent.

        Args:
            agent_id(str): Agent id
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Delete agent
            err = self._agent_repo.delete_agent(agent_id=agent_id, user_id=user_id)

        return err if err else None
