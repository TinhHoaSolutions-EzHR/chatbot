from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from app.models import ChatMessage
from app.models import ChatSession
from app.repositories.base import BaseRepository
from app.utils.api_response import APIError
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class ChatRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Chat repository class for handling chat-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_chat_sessions(self, user_id: str) -> Tuple[List[ChatSession], Optional[APIError]]:
        """
        Get all chat sessions of the user. Sort by updated_at in descending order.

        Args:
            user_id(str): User id

        Returns:
            Tuple[List[ChatSession], Optional[APIError]]: List of chat session objects and APIError object if any error
        """
        try:
            chat_sessions = (
                self._db_session.query(ChatSession)
                .filter(ChatSession.user_id == user_id)
                .order_by(ChatSession.updated_at.desc())
                .all()
            )
            return chat_sessions, None
        except Exception as e:
            logger.error(f"Error getting chat sessions: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_chat_messages(self, chat_session_id: str, user_id: str) -> Tuple[List[ChatSession], Optional[APIError]]:
        """
        Get all chat messages of the chat session. Sort by created_at in ascending order.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[List[ChatSession], Optional[APIError]]: List of chat session objects and APIError object if any error
        """
        try:
            chat_messages = (
                self._db_session.query(ChatMessage)
                .filter(and_(ChatMessage.chat_session_id == chat_session_id, ChatMessage.user_id == user_id))
                .join(ChatSession, ChatMessage.chat_session_id == ChatSession.id)
                .order_by(ChatMessage.created_at.asc())
                .all()
            )
            return chat_messages, None
        except Exception as e:
            logger.error(f"Error getting chat messages: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_chat_session(self, chat_session_id: str, user_id: str) -> Tuple[ChatSession, Optional[APIError]]:
        """
        Get chat session by id.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[ChatSession, Optional[APIError]]: Chat session object and APIError object if any error
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

    def get_chat_message(
        self, chat_message_id: str, chat_session_id: str, user_id: str
    ) -> Tuple[ChatMessage, Optional[APIError]]:
        """
        Get chat message by id.

        Args:
            chat_message_id(str): Message id
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[ChatMessage, Optional[APIError]]: Chat message object and APIError object if any error
        """
        try:
            chat_message = (
                self._db_session.query(ChatMessage)
                .filter(
                    and_(
                        ChatMessage.id == chat_message_id,
                        ChatMessage.chat_session_id == chat_session_id,
                        ChatMessage.user_id == user_id,
                    )
                )
                .first()
            )
            return chat_message, None
        except Exception as e:
            logger.error(f"Error getting chat message: {e}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_chat_session(self, chat_session: ChatSession) -> Optional[APIError]:
        """
        Create chat session.

        Args:
            chat_session(ChatSession): Chat session object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(chat_session)
            return None
        except Exception as e:
            logger.error(f"Error creating chat session: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_chat_message(self, chat_message: ChatMessage) -> Optional[APIError]:
        """
        Create chat message.

        Args:
            chat_message(ChatMessage): Chat message object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(chat_message)
            return None
        except Exception as e:
            logger.error(f"Error creating chat message: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_chat_session(self, chat_session_id: str, chat_session: ChatSession, user_id: str) -> Optional[APIError]:
        """
        Update chat session.

        Args:
            chat_session_id(str): Chat session id
            chat_session(ChatSession): Chat session object
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
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
        self, chat_session_id: str, chat_message_id: str, chat_message: ChatMessage, user_id: str
    ) -> Optional[APIError]:
        """
        Update chat message.

        Args:
            chat_session_id(str): Chat session id
            chat_message_id(str): Chat message id
            chat_message(ChatMessage): Chat message object
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            chat_message = {key: value for key, value in chat_message.__dict__.items() if not key.startswith("_")}
            self._db_session.query(ChatMessage).filter(
                and_(
                    ChatMessage.id == chat_message_id,
                    ChatMessage.chat_session_id == chat_session_id,
                    ChatMessage.user_id == user_id,
                )
            ).update(chat_message)
            return None
        except Exception as e:
            logger.error(f"Error updating chat message: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_chat_session(self, chat_session_id: str, user_id: str) -> Optional[APIError]:
        """
        Delete chat session by id.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
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

    def delete_chat_message(self, chat_message_id: str, chat_session_id: str, user_id: str) -> Optional[APIError]:
        """
        Delete chat message by id.

        Args:
            chat_message_id(str): Message id
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(ChatMessage).filter(
                and_(
                    ChatMessage.id == chat_message_id,
                    ChatMessage.chat_session_id == chat_session_id,
                    ChatMessage.user_id == user_id,
                )
            ).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting chat message: {e}")
            self._db_session.rollback()
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)