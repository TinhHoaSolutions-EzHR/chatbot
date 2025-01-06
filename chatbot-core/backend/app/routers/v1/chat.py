from collections.abc import Generator

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models import User
from app.models.chat import ChatFeedbackRequest
from app.models.chat import ChatMessageRequest
from app.models.chat import ChatMessageRequestType
from app.models.chat import ChatMessageResponse
from app.models.chat import ChatSessionRequest
from app.models.chat import ChatSessionResponse
from app.services.chat import ChatService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger
from app.utils.user.authentication import get_current_user


logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["chat", "session", "message"])


@router.get("/chat-sessions", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_chat_sessions(
    db_session: Session = Depends(get_db_session), user: User = Depends(get_current_user)
) -> BackendAPIResponse:
    """
    Get all chat sessions of the user.

    Args:
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object

    Returns:
        BackendAPIResponse: API response.
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Get chat sessions of user
    chat_sessions, err = ChatService(db_session=db_session).get_chat_sessions(user_id=user.id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse chat sessions
    if chat_sessions:
        data = [ChatSessionResponse.model_validate(chat_session) for chat_session in chat_sessions]
    else:
        data = []

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.get(
    "/chat-sessions/{chat_session_id}", response_model=APIResponse, status_code=status.HTTP_200_OK
)
def get_chat_session(
    chat_session_id: str,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> BackendAPIResponse:
    """
    Get chat session by id.

    Args:
        chat_session_id (str): Chat session id.
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object.

    Returns:
        BackendAPIResponse: API response.
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Get chat session
    chat_session, err = ChatService(db_session=db_session).get_chat_session(
        chat_session_id=chat_session_id, user_id=user.id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse chat session
    if chat_session:
        chat_messages, err = ChatService(db_session=db_session).get_chat_messages(
            chat_session_id=chat_session_id, user_id=user.id
        )
        if err:
            status_code, detail = err.kind
            raise HTTPException(status_code=status_code, detail=detail)

        data = ChatSessionResponse.model_validate(chat_session)
        data.messages = [
            ChatMessageResponse.model_validate(chat_message) for chat_message in chat_messages
        ]
    else:
        data = None

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.post("/chat-sessions", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_chat_session(
    chat_session_request: ChatSessionRequest,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> BackendAPIResponse:
    """
    Create chat session.

    Args:
        chat_session_request (ChatSessionRequest): Chat session request object.
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object.

    Returns:
        BackendAPIResponse: API response
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Create chat session
    chat_session, err = ChatService(db_session=db_session).create_chat_session(
        chat_session_request=chat_session_request, user_id=user.id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    if chat_session:
        data = ChatSessionResponse.model_validate(chat_session)
    else:
        data = None

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.patch(
    "/chat-sessions/{chat_session_id}", response_model=APIResponse, status_code=status.HTTP_200_OK
)
def update_chat_session(
    chat_session_id: str,
    chat_session_request: ChatSessionRequest,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> BackendAPIResponse:
    """
    Update chat session.

    Args:
        chat_session_id (str): Chat session id.
        chat_session_request (ChatSessionRequest): Chat session request object.
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object.

    Returns:
        BackendAPIResponse: API response
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Update chat session
    err = ChatService(db_session=db_session).update_chat_session(
        chat_session_id=chat_session_id, chat_session_request=chat_session_request, user_id=user.id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = chat_session_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.delete("/chat-sessions/{chat_session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_session(
    chat_session_id: str,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> None:
    """
    Delete chat session.

    Args:
        chat_session_id (str): Chat session id.
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object.
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Delete chat session
    err = ChatService(db_session=db_session).delete_chat_session(
        chat_session_id=chat_session_id, user_id=user.id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)


@router.post(
    "/chat-sessions/{chat_session_id}/messages",
    status_code=status.HTTP_201_CREATED,
)
def handle_new_chat_message(
    chat_session_id: str,
    chat_message_request: ChatMessageRequest,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> StreamingResponse:
    """
    This endpoint is both used for all the following purposes:
    - Sending a new message in the session
    - Regenerating a message in the session (just send the same one again)
    - Editing a message (similar to regenerating but sending a different message)

    Args:
        chat_session_id (str): Chat session id.
        chat_message_request (ChatMessageRequest): Chat message request object.
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object.

    Returns:
        StreamingResponse: Streams the response to the new chat message.
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    if (
        chat_message_request.request_type != ChatMessageRequestType.REGENERATE
        and not chat_message_request.message
    ):
        status_code, detail = ErrorCodesMappingNumber.EMPTY_CHAT_MESSAGE
        raise HTTPException(status_code=status_code, detail=detail)

    # Generate the content
    content = ChatService(db_session=db_session).generate_stream_chat_message(
        chat_message_request=chat_message_request, chat_session_id=chat_session_id, user_id=user.id
    )
    if not isinstance(content, Generator):
        status_code, detail = content
        raise HTTPException(status_code=status_code, detail=detail)

    return StreamingResponse(content=content, media_type="text/event-stream")


@router.post("/feedback", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_chat_feedback(
    chat_feedback_request: ChatFeedbackRequest,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> BackendAPIResponse:
    """
    Create chat feedback.

    Args:
        chat_feedback_request (ChatFeedbackRequest): Chat feedback request object.
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object.

    Returns:
        BackendAPIResponse: API response
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(status_code=status_code, detail=detail)

    # Create chat feedback
    err = ChatService(db_session=db_session).create_chat_feedback(chat_feedback_request)

    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse response
    data = chat_feedback_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )
