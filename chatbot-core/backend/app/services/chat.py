from sqlalchemy.orm import Session
from typing import Tuple, List

from app.models.api import APIError
from app.models.chat import ChatSession, ChatSessionRequest
from app.repositories.chat import ChatRepository
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class ChatService:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def get_chat_sessions(self, user_id: str) -> Tuple[List[ChatSession], APIError | None]:
        """
        Get all chat sessions of the user.

        Args:
            user_id(str): User id

        Returns:
            Tuple[List[ChatSession], APIError | None]: List of chat session objects and APIError object if any error
        """
        return ChatRepository(db_session=self._db_session).get_chat_sessions(user_id=user_id)

    def get_chat_session(self, id: str, user_id: str) -> Tuple[ChatSession, APIError | None]:
        """
        Get chat session by id.

        Args:
            id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[ChatSession, APIError | None]: Chat session object and APIError object if any error
        """
        return ChatRepository(db_session=self._db_session).get_chat_session(id=id, user_id=user_id)

    def create_chat_session(
        self, chat_session_request: ChatSessionRequest, user_id: str
    ) -> APIError | None:
        """
        Create chat session.

        Args:
            chat_session_request(ChatSessionRequest): Chat session request object
            user_id(str): User id

        Returns:
            APIError | None: APIError object if any error
        """
        err = None
        try:
            # Begin transaction
            self._db_session.begin()

            # Define chat session
            chat_session = ChatSession(
                user_id=user_id,
                persona_id=chat_session_request.persona_id,
                description=chat_session_request.description,
            )

            # Create chat session
            err = ChatRepository(db_session=self._db_session).create_chat_session(
                chat_session=chat_session
            )
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error creating chat session: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    def update_chat_session(
        self, id: str, chat_session_request: ChatSessionRequest, user_id: str
    ) -> APIError | None:
        """
        Update chat session.

        Args:
            id(str): Chat session id
            chat_session_request(ChatSessionRequest): Chat session request object
            user_id(str): User id

        Returns:
            APIError | None: APIError object if any error
        """
        err = None
        try:
            # Begin transaction
            self._db_session.begin()

            # Define chat session
            chat_session = ChatSession(
                description=chat_session_request.description,
            )

            # Update chat session
            err = ChatRepository(db_session=self._db_session).update_chat_session(
                id=id, chat_session=chat_session, user_id=user_id
            )
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error updating chat session: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    def delete_chat_session(self, id: str, user_id: str) -> APIError | None:
        """
        Delete chat session by id.

        Args:
            id(str): Chat session id
            user_id(str): User id

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            # Begin transaction
            self._db_session.begin()

            # Delete chat session
            err = ChatRepository(db_session=self._db_session).delete_chat_session(
                id=id, user_id=user_id
            )
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error deleting chat session: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    def get_chat_message(self, chat_message_id: str, user_id: str):
        # TODO: user_id is just for check whether the user can access the chat message or not
        pass
