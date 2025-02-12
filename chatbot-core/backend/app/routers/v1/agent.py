from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.databases.minio import get_minio_connector
from app.databases.minio import MinioConnector
from app.databases.mssql import get_db_session
from app.models import User
from app.models.agent import AgentRequest
from app.models.agent import AgentResponse
from app.services.agent import AgentService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger
from app.utils.user.authentication import get_current_user_from_token


logger = get_logger(__name__)
router = APIRouter(prefix="/agents", tags=["agent", "assistant"])


@router.get("", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_agents(
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user_from_token),
) -> BackendAPIResponse:
    """
    Get all agents.

    Args:
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object.

    Returns:
        BackendAPIResponse: API response with the list of agents.
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Get agents
    agents, err = AgentService(db_session=db_session).get_agents(user_id=user.id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse agents
    if agents:
        data = [AgentResponse.model_validate(agent) for agent in agents]
    else:
        data = []

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.get("/{agent_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_agent(
    agent_id: str,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user_from_token),
) -> BackendAPIResponse:
    """
    Get an agent by id.

    Args:
        agent_id (str): Agent id
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object.

    Returns:
        BackendAPIResponse: API response with the agent.
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Get agent
    agent, err = AgentService(db_session=db_session).get_agent(agent_id=agent_id, user_id=user.id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse agent
    if agent:
        data = AgentResponse.model_validate(agent)
    else:
        data = None

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_agent(
    agent_request: AgentRequest,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user_from_token),
) -> BackendAPIResponse:
    """
    Create a new agent.

    Args:
        agent_request (AgentRequest): Agent request object (required).
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object (required).

    Returns:
        BackendAPIResponse: API response with the created agent.
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Create agent
    err = AgentService(db_session=db_session).create_agent(
        agent_request=agent_request,
        user_id=str(user.id),
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse agent
    data = agent_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.patch("/{agent_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_agent(
    agent_id: str,
    agent_request: AgentRequest,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user_from_token),
) -> BackendAPIResponse:
    """
    Update an agent.

    Args:
        agent_id (str): Agent id
        agent_request (AgentRequest): Agent request object.
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object.

    Returns:
        BackendAPIResponse: API response with the updated agent.
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Update agent
    err = AgentService(db_session=db_session).update_agent(
        agent_id=agent_id,
        agent_request=agent_request,
        user_id=user.id,
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse agent
    data = agent_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(
    agent_id: str,
    db_session: Session = Depends(get_db_session),
    minio_connector: MinioConnector = Depends(get_minio_connector),
    user: User = Depends(get_current_user_from_token),
) -> None:
    """
    Delete an agent.

    Args:
        agent_id (str): Agent id
        db_session (Session): Database session. Defaults to relational database session.
        minio_connector (MinioConnector): Minio connector object
        user (User): User object.

    Returns:
        None
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Delete agent
    err = AgentService(db_session=db_session, minio_connector=minio_connector).delete_agent(
        agent_id=agent_id, user_id=user.id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)
