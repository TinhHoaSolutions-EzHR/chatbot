from collections.abc import Generator
from typing import List
from typing import Tuple
from typing import Union

from sqlalchemy.orm import Session

from app.models.api import APIError
from app.models.chat import ChatMessage
from app.models.chat import ChatMessageRequest
from app.models.chat import ChatSession
from app.models.chat import ChatSessionRequest
from app.repositories.agent import AgentRepository
from app.repositories.chat import ChatRepository
from app.utils.error_handler import ErrorCodesMappingNumber
from app.utils.logger import LoggerFactory
# from app.models.prompt import Prompt
# from app.repositories.prompt import PromptRepository

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

    def get_chat_messages(self, chat_session_id: str, user_id: str) -> Tuple[List[ChatMessage], APIError | None]:
        """
        Get all chat messages of the chat session.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User ids

        Returns:
            Tuple[List[ChatMessage], APIError | None]: List of chat message objects and APIError object if any error
        """
        return ChatRepository(db_session=self._db_session).get_chat_messages(
            chat_session_id=chat_session_id, user_id=user_id
        )

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
                agent_id=chat_session_request.agent_id,
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

    def _create_chat_chain(
        self, chat_session_id: str, user_id: str, stop_at_message_id: str
    ) -> Tuple[Tuple[str, str], Union[APIError, None]]:
        chat_messages, err = self.get_chat_messages(chat_session_id=chat_session_id, user_id=user_id)
        if not chat_messages or err:
            return (None, None), APIError(kind=ErrorCodesMappingNumber.CHAT_MESSAGES_NOT_FOUND.value)

        chat_id_to_chat_message = {chat_message.id: chat_messages for chat_message in chat_messages}
        root_message = chat_messages[0]
        mainline_messages: list[ChatMessage] = []
        current_message = root_message
        while current_message:
            child_message_id = current_message.latest_child_message_id

            if not child_message_id or child_message_id == stop_at_message_id:
                break
            current_message = chat_id_to_chat_message.get(child_message_id)
            mainline_messages.append(current_message)

        return (mainline_messages[-1], mainline_messages[:-1]), None

    def generate_stream_chat_message(
        self, chat_message_request: ChatMessageRequest, chat_session_id: str, user_id: str
    ) -> Union[Generator[str, None, None], Union[APIError, None]]:
        # Get the chat session
        chat_session, err = self.get_chat_session(chat_session_id=chat_session_id, user_id=user_id)
        if err:
            return err

        chat_message_request.message
        chat_message_request.parent_message_id

        # Get the agent
        alternate_agent_id = chat_message_request.alternate_agent_id
        if alternate_agent_id:
            # Allows users to specify a temporary agent in the chat session
            agent, err = AgentRepository(db_session=self._db_session).get_agent(agent_id=alternate_agent_id)
            if err:
                return err
        else:
            agent = chat_session.agent

        if not agent:
            return APIError(kind=ErrorCodesMappingNumber.AGENT_NOT_FOUND.value)

        # # If a prompt override is specified via the API, use that with highest priority
        # prompt_id = chat_message_request.prompt_id
        # if not prompt_id and agent.prompts:
        #     # If the agent has prompts, use one with the flag default_prompt set to True
        #     prompt_criteria = and_(Prompt.user_id.is_(None), Prompt.is_default_prompt.is_(True))
        #     prompt, err = PromptRepository(db_session=self._db_session).get_prompt_by_criteria(criteria=prompt_criteria)
        #     if err:
        #         return err
        #     prompt_id = prompt.id

        # if chat_message_request.is_regenerated:
        #     final_msg, history_msg = self._create_chat_chain(
        #         chat_session_id=chat_session_id, user_id=user_id, stop_at_message_id=parent_message_id
        #     )

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
