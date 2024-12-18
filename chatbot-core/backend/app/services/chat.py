from collections.abc import Generator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from sqlalchemy.orm import Session

from app.models import ChatMessage
from app.models import ChatSession
from app.models.chat import ChatMessageRequest
from app.models.chat import ChatMessageRequestType
from app.models.chat import ChatMessageType
from app.models.chat import ChatSessionRequest
from app.repositories.chat import ChatRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ConversationError
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class ChatService(BaseService):
    def __init__(self, db_session: Session) -> None:
        """
        Chat service class for handling chat-related operations.

        Args:
            db_session(Session): Database session
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._chat_repository = ChatRepository(db_session=self._db_session)

    def get_chat_sessions(self, user_id: str) -> Tuple[List[ChatSession], Optional[APIError]]:
        """
        Get all chat sessions of the user.

        Args:
            user_id(str): User id

        Returns:
            Tuple[List[ChatSession], Optional[APIError]]: List of chat session objects and APIError object if any error
        """
        return self._chat_repository.get_chat_sessions(user_id=user_id)

    def get_chat_session(
        self, chat_session_id: str, user_id: str
    ) -> Tuple[ChatSession, Optional[APIError]]:
        """
        Get chat session by id.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[ChatSession, Optional[APIError]]: Chat session object and APIError object if any error
        """
        chat_session, err = self._chat_repository.get_chat_session(
            chat_session_id=chat_session_id, user_id=user_id
        )
        if err:
            return None, err

        chat_messages, err = self._chat_repository.get_chat_messages(
            chat_session_id=chat_session_id, user_id=user_id
        )
        if err:
            return None, err

        # Set chat messages to the chat session
        chat_session.chat_messages = chat_messages

        return chat_session, None

    def create_chat_session(
        self, chat_session_request: ChatSessionRequest, user_id: str
    ) -> Optional[APIError]:
        """
        Create chat session.

        Args:
            chat_session_request(ChatSessionRequest): Chat session request object
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define chat session
            chat_session = ChatSession(
                user_id=user_id,
                agent_id=chat_session_request.agent_id,
                description=chat_session_request.description,
            )

            # Create chat session
            err = self._chat_repository.create_chat_session(chat_session=chat_session)

        return err if err else None

    def update_chat_session(
        self, chat_session_id: str, chat_session_request: ChatSessionRequest, user_id: str
    ) -> Optional[APIError]:
        """
        Update chat session.

        Args:
            chat_session_id(str): Chat session id
            chat_session_request(ChatSessionRequest): Chat session request object
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define chat session
            chat_session = ChatSession(
                description=chat_session_request.description,
                agent_id=chat_session_request.agent_id,
                shared_status=chat_session_request.shared_status,
                current_alternate_model=chat_session_request.current_alternate_model,
            )

            # Update chat session
            err = self._chat_repository.update_chat_session(
                chat_session_id=chat_session_id, chat_session=chat_session, user_id=user_id
            )

        return err if err else None

    def delete_chat_session(self, chat_session_id: str, user_id: str) -> Optional[APIError]:
        """
        Delete chat session by id.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Delete chat session
            err = self._chat_repository.delete_chat_session(
                chat_session_id=chat_session_id, user_id=user_id
            )

        return err if err else None

    def _update_message_chain(
        self,
        chat_session_id: str,
        user_id: str,
        parent_message_id: Optional[str] = None,
        child_message_id: Optional[str] = None,
    ) -> Optional[APIError]:
        """
        Update message chain.
        Update the parent message with the child message id and the child message with the parent message id.

        E.g: Assume we have a message chain as follows:
            A -> B -> C
        If we want to delete B, we need to update A and C as follows:
            A -> C
        This means the child message id of A is C and the parent message id of C is A.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id
            parent_message_id(str): Parent message id
            child_message_id(str): Child message id

        Returns:
            Optional[APIError]: APIError object if any error
        """
        # Update parent message's child reference
        if parent_message_id:
            parent_updated_message = ChatMessage(child_message_id=child_message_id)
            err = self._chat_repository.update_chat_message(
                chat_session_id=chat_session_id,
                chat_message_id=parent_message_id,
                chat_message=parent_updated_message,
                user_id=user_id,
            )
            if err:
                return err

        # Update child message's parent reference
        if child_message_id:
            child_updated_message = ChatMessage(parent_message_id=parent_message_id)
            err = self._chat_repository.update_chat_message(
                chat_session_id=chat_session_id,
                chat_message_id=child_message_id,
                chat_message=child_updated_message,
                user_id=user_id,
            )
            if err:
                return err

    def _make_chat_request(
        self,
        user_id: str,
        chat_session_id: str,
        message: str,
        message_type: ChatMessageType,
        latest_chat_response: Optional[ChatMessage] = None,
    ) -> Tuple[ChatMessage, Optional[APIError]]:
        """
        Make chat request message.

        Args:
            user_id(str): User id
            chat_session_id(str): Chat session id
            message(str): Message text
            message_type(ChatMessageType): Message type
            latest_chat_response(ChatMessage): Latest chat response message. Defaults to None

        Returns:
            Tuple[ChatMessage, Optional[APIError]]: Chat request message and APIError object if any error
        """
        # Define the parent message id as the latest chat response id (if any)
        parent_message_id = latest_chat_response.id if latest_chat_response else None

        # Create chat request message
        new_chat_request = ChatMessage(
            user_id=user_id,
            chat_session_id=chat_session_id,
            parent_message_id=parent_message_id,
            message=message,
            message_type=message_type,
        )

        # Create chat request message
        err = self._chat_repository.create_chat_message(chat_message=new_chat_request)
        if err:
            return None, err

        # Flush the session to send the data to the database (but do not commit yet)
        self._db_session.flush()

        # Update the child_message_id of the latest chat response (if any)
        if latest_chat_response:
            logger.info("Updating the child_message_id of the latest chat response message")
            latest_updated_chat_response = ChatMessage(child_message_id=new_chat_request.id)
            err = self._chat_repository.update_chat_message(
                chat_session_id=chat_session_id,
                chat_message_id=latest_chat_response.id,
                chat_message=latest_updated_chat_response,
                user_id=user_id,
            )
            if err:
                return None, err

        return new_chat_request, None

    def _generate_chat_response(
        self,
        chat_message_request: ChatMessageRequest,
        chat_session_id: str,
        user_id: str,
        current_request_id: str,
    ) -> Tuple[ChatMessage, Optional[APIError]]:
        """
        Generate chat response message.
        The input message is used to query the LLM model and generate the response message.

        Args:
            chat_message_request(ChatMessageRequest): Chat message request object
            chat_session_id(str): Chat session id
            user_id(str): User id
            current_request_id(str): Current request message id
            latest_response_id(str): Latest response message id. Defaults to None

        Returns:
            Tuple[Union[ChatMessage, None], Optional[APIError]]: Chat response message and APIError object if any error
        """
        # Generate chat response
        # TODO: Implement the logic to query the LLM model and generate the response
        response_message = chat_message_request.message + " (Response)"
        current_chat_response = ChatMessage(
            user_id=user_id,
            chat_session_id=chat_session_id,
            parent_message_id=current_request_id,
            message=response_message,
            message_type=ChatMessageType.ASSISTANT,
        )

        err = self._chat_repository.create_chat_message(chat_message=current_chat_response)
        if err:
            return None, err

        return current_chat_response, err

    def _delete_messages_and_update_chain(
        self,
        chat_session_id: str,
        user_id: str,
        current_chat_request: Optional[ChatMessage] = None,
        current_chat_response: Optional[ChatMessage] = None,
    ) -> Optional[APIError]:
        """
        Delete messages and update the message chain.

        E.g: Assume we have a message chain as follows:
            A -> B -> C
        If we want to delete B, we need to update A and C as follows:
            A -> C
        This means the child message id of A is C and the parent message id of C is A.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id
            current_chat_request(ChatMessage): Current chat request message
            current_chat_response(ChatMessage): Current chat response

        Returns:
            Optional[APIError]: APIError object if any error
        """
        # Get the parent and child message ids of the current response message
        parent_request_message_id = None
        child_response_message_id = None

        # Delete the current request message
        if current_chat_request:
            parent_request_message_id = current_chat_request.parent_message_id
            err = self._chat_repository.delete_chat_message(
                chat_message_id=current_chat_request.id,
                chat_session_id=chat_session_id,
                user_id=user_id,
            )
            if err:
                return err

        # Delete the current response message
        if current_chat_response:
            child_response_message_id = current_chat_response.child_message_id
            err = self._chat_repository.delete_chat_message(
                chat_message_id=current_chat_response.id,
                chat_session_id=chat_session_id,
                user_id=user_id,
            )
            if err:
                return err

        # Update the message chain
        if parent_request_message_id and child_response_message_id:
            logger.info(
                "Updating the child_message_id of the parent of the request message, parent_message_id of the next child message"
            )
            # Update the child_message_id of the parent of the request message, parent_message_id of the next child message
            err = self._update_message_chain(
                chat_session_id=chat_session_id,
                user_id=user_id,
                parent_message_id=parent_request_message_id,
                child_message_id=child_response_message_id,
            )
        elif parent_request_message_id:
            logger.info("Updating the parent request message with the new child message id")
            # Update the parent request message with the new child message id
            err = self._update_message_chain(
                chat_session_id=chat_session_id,
                user_id=user_id,
                parent_message_id=parent_request_message_id,
            )
        elif child_response_message_id:
            logger.info("Updating the next child message with the new parent message id")
            # Update the next child message with the new parent message id
            err = self._update_message_chain(
                chat_session_id=chat_session_id,
                user_id=user_id,
                child_message_id=child_response_message_id,
            )
        else:
            err = None

        if err:
            return err

        return None

    def _handle_existing_chat_message(
        self, chat_message_request: ChatMessageRequest, chat_session_id: str, user_id: str
    ) -> Tuple[Optional[ChatMessage], Optional[APIError]]:
        """
        Handle existing chat message, either regenerate or edit the message.
        In this scenario, we will delete the existing response message (if any) and its corresponding request message.
        If the request is regenerated, we will keep the old request message and specify as new message in our chat session.
        If the request is edited, we simply consider the edited message as the new message in our chat session.

        Args:
            chat_message_request(ChatMessageRequest): Chat message request object
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[Union[str, None], Optional[APIError]]: Chat response message and APIError object if any error
        """
        # Get the current chat message and its parent / child message (based on the message message)
        current_chat_message, err = self._chat_repository.get_chat_message(
            chat_message_id=chat_message_request.id,
            chat_session_id=chat_session_id,
            user_id=user_id,
        )
        if err:
            return None, err

        # Define the current chat request and response
        # When regenerating or editing message, we need to care about the couple of request and response messages
        if current_chat_message.message_type == ChatMessageType.USER:
            logger.info(
                "Editing the existing request message. Current chat message is a request message."
            )
            # When the message is edited, the chat request is the current message
            current_chat_request = current_chat_message
            current_chat_response, err = self._chat_repository.get_chat_message(
                chat_message_id=current_chat_message.child_message_id,
                chat_session_id=chat_session_id,
                user_id=user_id,
            )
            if err:
                return None, err
        elif current_chat_message.message_type == ChatMessageType.ASSISTANT:
            logger.info(
                "Regenerating the existing request message. Current chat message is a response message."
            )
            # When the message is regenerated, the chat response is the current message
            current_chat_response = current_chat_message
            current_chat_request, err = self._chat_repository.get_chat_message(
                chat_message_id=current_chat_message.parent_message_id,
                chat_session_id=chat_session_id,
                user_id=user_id,
            )

            # When the message is regenerated, keep the old request message and specify as new message in our chat session
            chat_message_request.message = current_chat_request.message
            if err:
                return None, err
        else:
            raise ConversationError(
                f"Message type must be either {ChatMessageType.USER} or {ChatMessageType.ASSISTANT}. Got {current_chat_message.message_type}"
            )

        # As we are regenerating the response, we delete the current response message and its request message
        # Then, deleting the response and corresponding request message (update the child_message_id of the parent of the request message, parent_message_id of the next child message)
        err = self._delete_messages_and_update_chain(
            chat_session_id=chat_session_id,
            user_id=user_id,
            current_chat_request=current_chat_request,
            current_chat_response=current_chat_response,
        )
        if err:
            return None, err

        # Flush the session to send the data to the database (but do not commit yet)
        self._db_session.flush()

        return current_chat_message, None

    def _handle_new_chat_message(
        self, chat_message_request: ChatMessageRequest, chat_session_id: str, user_id: str
    ) -> Tuple[Optional[str], Optional[APIError]]:
        """
        Handle new chat message in the chat session.

        Args:
            chat_message_request(ChatMessageRequest): Chat message request object
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Union[str, None] | Optional[APIError]: Chat response message or APIError object if any error
        """
        # Get the current chat messages in the chat session
        current_chat_messages, err = self._chat_repository.get_chat_messages(
            chat_session_id=chat_session_id, user_id=user_id
        )
        if err:
            return None, err

        # If there are no any chat messages, the request message is the first message
        latest_chat_response = None
        if current_chat_messages:
            logger.info("The chat session has existing messages.")
            # Get the latest chat message
            latest_chat_response = current_chat_messages[-1]

        # Create chat request message
        new_chat_request, err = self._make_chat_request(
            user_id=user_id,
            chat_session_id=chat_session_id,
            message=chat_message_request.message,
            message_type=ChatMessageType.USER,
            latest_chat_response=latest_chat_response,
        )
        if err:
            return None, err

        # Generate chat response
        chat_response, err = self._generate_chat_response(
            user_id=user_id,
            chat_message_request=chat_message_request,
            chat_session_id=chat_session_id,
            current_request_id=new_chat_request.id,
        )
        if err:
            return None, err

        # Flush the session to send the data to the database (but do not commit yet)
        self._db_session.flush()

        # Update the child_message_id of the current request message as the new response message
        updated_message = ChatMessage(child_message_id=chat_response.id)
        err = self._chat_repository.update_chat_message(
            chat_session_id=chat_session_id,
            chat_message_id=new_chat_request.id,
            chat_message=updated_message,
            user_id=user_id,
        )
        if err:
            return None, err

        return chat_response.message, None

    def generate_stream_chat_message(
        self, chat_message_request: ChatMessageRequest, chat_session_id: str, user_id: str
    ) -> Union[Generator[str, None, None], Optional[APIError]]:
        """
        Generate stream chat message for the new message request.

        Args:
            chat_message_request(ChatMessageRequest): Chat message request object
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Generator[str, None, None] | Optional[APIError]: Generator object or APIError object if any error
        """
        with self._transaction():
            # Get the current chat session
            chat_session, err = self._chat_repository.get_chat_session(
                chat_session_id=chat_session_id, user_id=user_id
            )
            if err:
                return err

            # Create chat session if it does not exist
            is_chat_session_exists = chat_session is not None
            if not is_chat_session_exists:
                logger.info(
                    f"Chat session does not exist. Creating a new chat session with id: {chat_session_id}"
                )
                chat_session = ChatSession(id=chat_session_id, user_id=user_id)
                err = self._chat_repository.create_chat_session(chat_session=chat_session)
                if err:
                    return err

            # Handle processing existing message (regenerate or edit the message)
            if chat_message_request.request_type == ChatMessageRequestType.REGENERATE:
                logger.info("Regenerating the existing chat message")
                existing_chat_request, err = self._handle_existing_chat_message(
                    chat_message_request=chat_message_request,
                    chat_session_id=chat_session_id,
                    user_id=user_id,
                )
                if err:
                    return err

                # Use the original message as the new message
                chat_message_request.message = existing_chat_request.message

            elif chat_message_request.request_type == ChatMessageRequestType.EDIT:
                logger.info("Editing the existing chat message")
                _, err = self._handle_existing_chat_message(
                    chat_message_request=chat_message_request,
                    chat_session_id=chat_session_id,
                    user_id=user_id,
                )
                if err:
                    return err

            # Handle processing new message (query the LLM and generate the response)
            chat_response, err = self._handle_new_chat_message(
                chat_message_request=chat_message_request,
                chat_session_id=chat_session_id,
                user_id=user_id,
            )
            if err:
                return err

        yield chat_response
