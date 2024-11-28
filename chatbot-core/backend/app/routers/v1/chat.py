from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Generator

from app.databases.postgres import get_db_session
from app.models.api import APIResponse
from app.models.chat import ChatSessionRequest, ChatSessionResponse, ChatMessageRequest
from app.models.user import User
from app.services.chat import ChatService
from app.settings import Constants
from app.utils.api_response import BackendAPIResponse
from app.utils.logger import LoggerFactory
from app.utils.user_authentication import get_current_user


logger = LoggerFactory().get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["chat", "session", "message"])


@router.get("/chat-sessions", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_chat_sessions(
    db_session: Session = Depends(get_db_session), user: User | None = Depends(get_current_user)
) -> None:
    """
    Get all chat sessions of the user.

    Args:
        db_session (Session): Database session. Defaults to relational database session.
        user (User | None): User object
    """
    user_id = user.id if user else None

    # Get chat sessions of user
    chat_sessions, err = ChatService(db_session=db_session).get_chat_sessions(user_id=user_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse chat sessions
    chat_sessions_response = [
        ChatSessionResponse.model_validate(chat_session) for chat_session in chat_sessions
    ]
    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=chat_sessions_response)
        .respond()
    )


@router.get("/chat-session/{id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_chat_session(
    id: str,
    db_session: Session = Depends(get_db_session),
    user: User | None = Depends(get_current_user),
) -> None:
    """
    Get chat session by id.

    Args:
        id (str): Chat session id.
        db_session (Session): Database session. Defaults to relational database session.
        user (User | None): User object.
    """
    user_id = user.id if user else None

    # Get chat session
    chat_session, err = ChatService(db_session=db_session).get_chat_session(id=id, user_id=user_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse chat session
    chat_session_response = ChatSessionResponse.model_validate(chat_session)
    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=chat_session_response)
        .respond()
    )


@router.post("/chat-session", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_chat_session(
    chat_session_request: ChatSessionRequest,
    db_session: Session = Depends(get_db_session),
    user: User | None = Depends(get_current_user),
) -> None:
    """
    Create chat session.

    Args:
        chat_session_request (ChatSessionRequest): Chat session request object.
        db_session (Session): Database session. Defaults to relational database session.
        user (User | None): User object.
    """
    user_id = user.id if user else None

    # Create chat session
    err = ChatService(db_session=db_session).create_chat_session(
        chat_session_request=chat_session_request, user_id=user_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).respond()


@router.put("/chat-session/{id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_chat_session(
    id: str,
    chat_session_request: ChatSessionRequest,
    db_session: Session = Depends(get_db_session),
    user: User | None = Depends(get_current_user),
) -> None:
    """
    Update chat session.

    Args:
        id (str): Chat session id.
        chat_session_request (ChatSessionRequest): Chat session request object.
        db_session (Session): Database session. Defaults to relational database session.
        user (User | None): User object.
    """
    user_id = user.id if user else None

    # Update chat session
    err = ChatService(db_session=db_session).update_chat_session(
        id=id, chat_session_request=chat_session_request, user_id=user_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).respond()


@router.delete("/chat-session/{id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def delete_chat_session(
    id: str,
    db_session: Session = Depends(get_db_session),
    user: User | None = Depends(get_current_user),
) -> None:
    """
    Delete chat session.

    Args:
        id (str): Chat session id.
        db_session (Session): Database session. Defaults to relational database session.
        user (User | None): User object.
    """
    user_id = user.id if user else None

    # Delete chat session
    err = ChatService(db_session=db_session).delete_chat_session(id=id, user_id=user_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).respond()


@router.post(
    "/chat-session/{id}/messages",
    status_code=status.HTTP_201_CREATED,
)
def handle_new_chat_message(
    id: str,
    chat_message_request: ChatMessageRequest,
    user: User | None = Depends(get_current_user),
) -> StreamingResponse:
    """
    This endpoint is both used for all the following purposes:
    - Sending a new message in the session
    - Regenerating a message in the session (just send the same one again)
    - Editing a message (similar to regenerating but sending a different message)

    Args:
        id (str): Chat session id.
        chat_message_request (ChatMessageRequest): Chat message request object.
        user (User | None): User object.

    Returns:
        StreamingResponse: Streams the response to the new chat message.
    """
    if not chat_message_request.message:
        # TODO: Implement a better error handler
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty"
        )

    def stream_generator() -> Generator[str, None, None]:
        # TODO: Implement the chat message handling logic
        yield "Message received"

    return StreamingResponse(content=stream_generator(), media_type="text/event-stream")


@router.put(
    "/chat-session/{chat_session_id}/messages/{message_id}/latest",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
)
def set_message_as_latest(
    chat_session_id: str,
    message_id: str,
    db_session: Session = Depends(get_db_session),
    user: User | None = Depends(get_current_user),
) -> None:
    user_id = user.id if user else None

    err = ChatService(db_session=db_session).set_message_as_latest(
        chat_session_id=chat_session_id, message_id=message_id, user_id=user_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).respond()
