from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from sqlalchemy.sql import or_

from app.models import Agent
from app.models.agent import AgentType
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class AgentRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Agent repository class for handling agent-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_agents(self, user_id: str) -> Tuple[Optional[List[Agent]], Optional[APIError]]:
        """
        Get all agents of the user.
        All agents include system agents and user-created agents.

        Args:
            user_id(str): User id

        Returns:
            Tuple[Optional[List[Agent]], Optional[APIError]]: List of agent objects and APIError object if any error
        """
        try:
            agents = (
                self._db_session.query(Agent)
                .filter(or_(Agent.user_id == user_id, Agent.agent_type == AgentType.SYSTEM))
                .all()
            )
            return agents, None
        except Exception as e:
            logger.error(f"Error getting agents: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_agent(self, agent_id: str, user_id: str) -> Tuple[Optional[Agent], Optional[APIError]]:
        """
        Get an agent by id. Include all system agents and user-created agents.

        Args:
            agent_id(str): Agent id
            user_id(str): User id

        Returns:
            Tuple[Optional[Agent], Optional[APIError]]: Agent object and APIError object if any error
        """
        try:
            agent = (
                self._db_session.query(Agent)
                .filter(
                    and_(
                        Agent.id == agent_id,
                        or_(Agent.user_id == user_id, Agent.agent_type == AgentType.SYSTEM),
                    )
                )
                .first()
            )
            return agent, None
        except Exception as e:
            logger.error(f"Error getting agent: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_agent(self, agent: Agent) -> Optional[APIError]:
        """
        Create a new agent.

        Args:
            agent(Agent): Agent object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(agent)
            return None
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_agent(
        self, agent_id: str, agent: Dict[str, Any], user_id: str
    ) -> Optional[APIError]:
        """
        Update an agent.
        Users can only update their own agents. For system agents, only owner, aka admin user, can update.

        Args:
            agent_id(str): Agent id
            agent(Dict[str, Any]): Agent object
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(Agent).filter(
                and_(Agent.id == agent_id, Agent.user_id == user_id)
            ).update(agent)
            return None
        except Exception as e:
            logger.error(f"Error updating agent: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_agent(self, agent_id: str, user_id: str) -> Optional[APIError]:
        """
        Delete an agent.
        Users can only delete their own agents. For system agents, only owner, aka admin user, can delete.

        Args:
            agent_id(str): Agent id
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(Agent).filter(
                and_(Agent.id == agent_id, Agent.user_id == user_id)
            ).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting agent: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
