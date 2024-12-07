from typing import List
from typing import Tuple
from typing import Union

from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.models.api import APIError
from app.repositories.base import BaseRepository
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class AgentRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Agent repository class for handling agent-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_agents(self) -> Tuple[List[Agent], Union[APIError, None]]:
        """
        Get all agents

        Returns:
            Tuple[List[Agent], Union[APIError, None]]: List of agent objects and APIError object if any error
        """
        try:
            agents = self._db_session.query(Agent).all()
            return agents, None
        except Exception as e:
            logger.error(f"Error getting agents: {e}", exc_info=True)
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_agent(self, agent_id: str) -> Tuple[Agent, Union[APIError, None]]:
        """
        Get agent by agent_id

        Args:
            agent_id(str): Agent id

        Returns:
            Tuple[Agent, Union[APIError, None]]: Agent object and APIError object if any error
        """
        try:
            agent = self._db_session.query(Agent).filter(Agent.id == agent_id).first()
            return agent, None
        except Exception as e:
            logger.error(f"Error getting agent: {e}", exc_info=True)
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
