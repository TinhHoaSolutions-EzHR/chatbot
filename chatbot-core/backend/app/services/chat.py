from sqlalchemy.orm import Session
from typing import Tuple, List, Generator

from app.models.api import APIError
from app.models.chat import ChatSession, ChatSessionRequest, ChatMessage, ChatMessageRequest
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

    def get_chat_messages(self, chat_session_id: str) -> Tuple[List[ChatMessage], APIError | None]:
        """
        Get all chat messages of the chat session.

        Args:
            chat_session_id(str): Chat session id

        Returns:
            Tuple[List[ChatMessage], APIError | None]: List of chat message objects and APIError object if any error
        """
        return ChatRepository(db_session=self._db_session).get_chat_messages(chat_session_id=chat_session_id)

    def get_chat_session(self, chat_session_id: str, user_id: str) -> Tuple[ChatSession, APIError | None]:
        """
        Get chat session by id.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[ChatSession, APIError | None]: Chat session object and APIError object if any error
        """
        return ChatRepository(db_session=self._db_session).get_chat_session(
            chat_session_id=chat_session_id, user_id=user_id
        )

    def get_chat_message(self, chat_session_id: str, chat_message_id: str) -> Tuple[ChatMessage, APIError | None]:
        """
        Get chat message by id.

        Args:
            chat_session_id(str): Chat session id
            chat_message_id(str): Chat message id

        Returns:
            Tuple[ChatMessage, APIError | None]: Chat message object and APIError object if any error
        """
        return ChatRepository(db_session=self._db_session).get_chat_message(
            chat_session_id=chat_session_id, chat_message_id=chat_message_id
        )

    def create_chat_session(self, chat_session_request: ChatSessionRequest, user_id: str) -> APIError | None:
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
            err = ChatRepository(db_session=self._db_session).create_chat_session(chat_session=chat_session)

            # Commit the transaction
            self._db_session.commit()
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error creating chat session: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    def update_chat_session(
        self, chat_session_id: str, chat_session_request: ChatSessionRequest, user_id: str
    ) -> APIError | None:
        """
        Update chat session.

        Args:
            chat_session_id(str): Chat session id
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
                chat_session_id=chat_session_id, chat_session=chat_session, user_id=user_id
            )

            # Commit the transaction
            self._db_session.commit()
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error updating chat session: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    def update_chat_message(
        self, chat_session_id: str, chat_message_id: str, chat_message_request: ChatMessageRequest
    ) -> APIError | None:
        """
        Update chat message.

        Args:
            chat_session_id(str): Chat session id
            chat_message_id(str): Chat message id
            chat_message_request(ChatMessageRequest): Chat message request object

        Returns:
            APIError | None: APIError object if any error
        """
        err = None
        try:
            # Begin the transaction
            self._db_session.begin()

            # Define the chat message
            chat_message = ChatMessage(
                message=chat_message_request.message,
                latest_child_message_id=chat_message_request.latest_child_message_id,
            )

            # Update the chat message
            err = ChatRepository(db_session=self._db_session).update_chat_message(
                chat_session_id=chat_session_id, chat_message_id=chat_message_id, chat_message=chat_message
            )

            # Commit the transaction
            self._db_session.commit()
        except Exception as e:
            # Rollback the transaction
            self._db_session.rollback()
            logger.error(f"Error updating chat message: {e}")
            err = APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

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
            # Begin transaction
            self._db_session.begin()

            # Delete chat session
            err = ChatRepository(db_session=self._db_session).delete_chat_session(
                chat_session_id=chat_session_id, user_id=user_id
            )

            # Commit the transaction
            self._db_session.commit()
        except Exception as e:
            # Rollback transaction
            self._db_session.rollback()
            logger.error(f"Error deleting chat session: {e}")
            return APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

        return err

    @classmethod
    def generate_stream_chat_message(cls) -> Generator[str, None, None]:
        # TODO: Implement the chat message handling logic
        yield "Message received"

    def set_message_as_latest(self, chat_session_id: str, chat_message_id: str, user_id: str) -> APIError | None:
        """
        Set message as latest.

        Args:
            chat_session_id(str): Chat session id
            message_id(str): Message id
            user_id(str): User id

        Returns:
            APIError | None: APIError object if any error
        """
        # Get the chat message
        chat_message, err = self.get_chat_message(chat_session_id=chat_session_id, chat_message_id=chat_message_id)
        if err:
            return err

        chat_user_id = chat_message.chat_session.user_id
        if not chat_user_id == user_id:
            return APIError(kind=ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value)

        # Get its parent message
        parent_message_id = chat_message.parent_message_id
        if not parent_message_id:
            raise RuntimeError(f"Trying to set a latest message without parent, message id: {chat_message.id}")
        parent_message, err = self.get_chat_message(chat_session_id=chat_session_id, chat_message_id=parent_message_id)
        if err:
            return err

        # Set the message as latest child of the parent message
        err = self.update_chat_message(
            chat_session_id=chat_session_id,
            chat_message_id=parent_message_id,
            chat_message_request=ChatMessageRequest(
                latest_child_message_id=chat_message_id,
            ),
        )
        return err
