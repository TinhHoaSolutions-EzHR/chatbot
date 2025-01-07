from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from app.models import ChatFeedback
from app.models import ChatMessage
from app.models import ChatSession
from app.repositories.base import BaseRepository
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class ChatRepository(BaseRepository):
    def __init__(self, db_session: Session):
        """
        Chat repository class for handling chat-related database operations.

        Args:
            db_session (Session): Database session
        """
        super().__init__(db_session=db_session)

    def get_chat_sessions(
        self, user_id: str, **filter
    ) -> Tuple[List[ChatSession], Optional[APIError]]:
        """
        Get all chat sessions of the user. Sort by updated_at in descending order.

        Args:
            user_id(str): User id
            **filter: Additional filters

        Returns:
            Tuple[List[ChatSession], Optional[APIError]]: List of chat session objects and APIError object if any error
        """
        try:
            query = self._db_session.query(ChatSession).filter(ChatSession.user_id == user_id)

            # Apply additional filters
            for field, value in filter.items():
                query = query.filter(getattr(ChatSession, field) == value)

            chat_sessions = query.order_by(ChatSession.updated_at.desc()).all()
            return chat_sessions, None
        except Exception as e:
            logger.error(f"Error getting chat sessions: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_chat_messages(
        self, chat_session_id: str, user_id: str
    ) -> Tuple[List[ChatMessage], Optional[APIError]]:
        """
        Get all chat messages of the chat session. Sort by created_at in ascending order.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[List[ChatMessage], Optional[APIError]]: List of chat message objects and APIError object if any error
        """
        try:
            chat_messages = (
                self._db_session.query(ChatMessage)
                .join(ChatSession, ChatMessage.chat_session_id == ChatSession.id)
                .filter(
                    and_(
                        ChatMessage.chat_session_id == chat_session_id,
                        ChatSession.user_id == user_id,
                    )
                )
                .order_by(ChatMessage.created_at.asc())
                .all()
            )
            return chat_messages, None
        except Exception as e:
            logger.error(f"Error getting chat messages: {e}")
            return [], APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def get_chat_session(
        self, chat_session_id: str, user_id: str
    ) -> Tuple[Optional[ChatSession], Optional[APIError]]:
        """
        Get chat session by id.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[Optional[ChatSession], Optional[APIError]]: Chat session object and APIError object if any error
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
    ) -> Tuple[Optional[ChatMessage], Optional[APIError]]:
        """
        Get chat message by id.

        Args:
            chat_message_id(str): Message id
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[Optional[ChatMessage], Optional[APIError]]: Chat message object and APIError object if any error
        """
        try:
            chat_message = (
                self._db_session.query(ChatMessage)
                .join(ChatSession, ChatMessage.chat_session_id == ChatSession.id)
                .filter(
                    and_(
                        ChatMessage.id == chat_message_id,
                        ChatMessage.chat_session_id == chat_session_id,
                        ChatSession.user_id == user_id,
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
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_chat_session(
        self, chat_session_id: str, chat_session: Dict[str, Any], user_id: str
    ) -> Optional[APIError]:
        """
        Update chat session.

        Args:
            chat_session_id(str): Chat session id
            chat_session(Dict[str, Any]): Chat session object
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.query(ChatSession).filter(
                and_(ChatSession.id == chat_session_id, ChatSession.user_id == user_id)
            ).update(chat_session)
            return None
        except Exception as e:
            logger.error(f"Error updating chat session: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def update_chat_message(
        self, chat_session_id: str, chat_message_id: str, chat_message: Dict[str, Any], user_id: str
    ) -> Optional[APIError]:
        """
        Update chat message.

        Args:
            chat_session_id(str): Chat session id
            chat_message_id(str): Chat message id
            chat_message( Dict[str, Any]): Chat message object
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            # Verify the chat session belongs to the user
            chat_session = (
                self._db_session.query(ChatSession)
                .filter(and_(ChatSession.id == chat_session_id, ChatSession.user_id == user_id))
                .first()
            )

            if not chat_session:
                return APIError(kind=ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value)

            # Update the chat message
            self._db_session.query(ChatMessage).filter(
                and_(
                    ChatMessage.id == chat_message_id,
                    ChatMessage.chat_session_id == chat_session_id,
                )
            ).update(chat_message)
            return None
        except Exception as e:
            logger.error(f"Error updating chat message: {e}")
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
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def delete_chat_message(
        self, chat_message_id: str, chat_session_id: str, user_id: str
    ) -> Optional[APIError]:
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
            # Verify the chat session belongs to the user
            chat_session = (
                self._db_session.query(ChatSession)
                .filter(and_(ChatSession.id == chat_session_id, ChatSession.user_id == user_id))
                .first()
            )

            if not chat_session:
                return APIError(kind=ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value)

            # Delete the chat message
            self._db_session.query(ChatMessage).filter(
                and_(
                    ChatMessage.id == chat_message_id,
                    ChatMessage.chat_session_id == chat_session_id,
                )
            ).delete()
            return None
        except Exception as e:
            logger.error(f"Error deleting chat message: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def create_chat_feedback(self, chat_feedback: ChatFeedback) -> Optional[APIError]:
        """
        Create chat feedback.

        Args:
            chat_feedback(ChatFeedback): Chat feedback object

        Returns:
            Optional[APIError]: APIError object if any error
        """
        try:
            self._db_session.add(chat_feedback)
            return None
        except Exception as e:
            logger.error(f"Error creating chat feedback: {e}", exc_info=True)
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)
