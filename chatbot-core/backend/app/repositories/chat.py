from typing import List
from typing import Tuple

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.api import APIError
from app.models.chat import ChatMessage
from app.models.chat import ChatSession
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class ChatRepository:
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
        try:
            chat_sessions = self._db_session.query(ChatSession).filter(ChatSession.user_id == user_id).all()
            return chat_sessions, None
        except Exception as e:
            logger.error(f"Error getting chat sessions: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_chat_messages(self, chat_session_id: str, user_id: str) -> Tuple[List[ChatSession], APIError | None]:
        """
        Get all chat messages of the chat session.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[List[ChatSession], APIError | None]: List of chat session objects and APIError object if any error
        """
        try:
            chat_messages = (
                self._db_session.query(ChatMessage)
                .filter(and_(ChatMessage.chat_session_id == chat_session_id, ChatSession.user_id == user_id))
                .all()
            )
            return chat_messages, None
        except Exception as e:
            logger.error(f"Error getting chat messages: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_chat_session(self, chat_session_id: str, user_id: str) -> Tuple[ChatSession, APIError | None]:
        """
        Get chat session by id.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[ChatSession, APIError | None]: Chat session object and APIError object if any error
        """
        try:
            chat_session = (
                self._db_session.query(ChatSession)
                .filter(and_(ChatSession.id == chat_session_id, ChatSession.user_id == user_id))
                .first()
            )
            return chat_session, None
        except Exception as e:
            logger.error(f"Error getting chat session: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_chat_message(self, chat_session_id: str, chat_message_id: str) -> Tuple[ChatMessage, APIError | None]:
        """
        Get chat message by id.

        Args:
            chat_session_id(str): Chat session id
            chat_message_id(str): Message id

        Returns:
            Tuple[ChatMessage, APIError | None]: Chat message object and APIError object if any error
        """
        try:
            chat_message = (
                self._db_session.query(ChatMessage)
                .filter(and_(ChatSession.id == chat_session_id, ChatMessage.id == chat_message_id))
                .first()
            )
            return chat_message, None
        except Exception as e:
            logger.error(f"Error getting chat message: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_chat_session(self, chat_session: ChatSession) -> APIError | None:
        """
        Create chat session.

        Args:
            chat_session(ChatSession): Chat session object

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            self._db_session.add(chat_session)
            return None
        except Exception as e:
            logger.error(f"Error creating chat session: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_chat_session(self, chat_session_id: str, chat_session: ChatSession, user_id: str) -> APIError | None:
        """
        Update chat session.

        Args:
            chat_session_id(str): Chat session id
            chat_session(ChatSession): Chat session object
            user_id(str): User id

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            chat_session = {key: value for key, value in chat_session.__dict__.items() if not key.startswith("_")}
            self._db_session.query(ChatSession).filter(
                and_(ChatSession.id == chat_session_id, ChatSession.user_id == user_id)
            ).update(chat_session)
            return None
        except Exception as e:
            logger.error(f"Error updating chat session: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_chat_message(
        self, chat_session_id: str, chat_message_id: str, chat_message: ChatMessage
    ) -> APIError | None:
        """
        Update chat message.

        Args:
            chat_session_id(str): Chat session id
            chat_message_id(str): Chat message id
            chat_message(ChatMessage): Chat message object

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            chat_message = {key: value for key, value in chat_message.__dict__.items() if not key.startswith("_")}
            self._db_session.query(ChatMessage).filter(
                and_(ChatSession.id == chat_session_id, ChatMessage.id == chat_message_id)
            ).update(chat_message)
            return None
        except Exception as e:
            logger.error(f"Error updating chat message: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_chat_session(self, chat_session_id: str, user_id: str) -> APIError | None:
        """
        Delete chat session by id.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            APIError | None: APIError object if any error
        """
        try:
            self._db_session.query(ChatSession).filter(
                and_(ChatSession.id == chat_session_id, ChatSession.user_id == user_id)
            ).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting chat session: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
