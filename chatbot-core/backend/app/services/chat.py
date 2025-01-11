from collections.abc import Generator
from typing import List
from typing import Optional
from typing import Tuple

import openai
from openai.types.chat import ChatCompletionChunk
from sqlalchemy.orm import Session

from app.models import ChatFeedback
from app.models import ChatMessage
from app.models import ChatSession
from app.models.chat import ChatFeedbackRequest
from app.models.chat import ChatMessageRequest
from app.models.chat import ChatMessageRequestType
from app.models.chat import ChatMessageResponse
from app.models.chat import ChatMessageType
from app.models.chat import ChatSessionRequest
from app.models.chat import ChatStreamResponse
from app.models.chat import ChatStreamType
from app.repositories.chat import ChatRepository
from app.services.base import BaseService
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ConversationError
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class ChatService(BaseService):
    def __init__(self, db_session: Session):
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
    ) -> Tuple[Optional[ChatSession], Optional[APIError]]:
        """
        Get chat session by id.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[Optional[ChatSession], Optional[APIError]]: Chat session object and APIError object if any error
        """
        return self._chat_repository.get_chat_session(
            chat_session_id=chat_session_id, user_id=user_id
        )

    def get_chat_messages(
        self, chat_session_id: str, user_id: str
    ) -> Tuple[List[ChatMessage], Optional[APIError]]:
        """
        Get all chat messages of the chat session.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id

        Returns:
            Tuple[List[ChatMessage], Optional[APIError]]: List of chat message objects and APIError object if any error
        """
        return self._chat_repository.get_chat_messages(
            chat_session_id=chat_session_id, user_id=user_id
        )

    def create_chat_session(
        self, chat_session_request: ChatSessionRequest, user_id: str
    ) -> Tuple[Optional[ChatSession], Optional[APIError]]:
        """
        Create chat session.

        Args:
            chat_session_request(ChatSessionRequest): Chat session request object
            user_id(str): User id

        Returns:
            Tuple[Optional[ChatSession], Optional[APIError]]: Chat session object and APIError object if any error.
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
            if err:
                return None, err

        return chat_session, None

    def update_chat_session(
        self, chat_session_id: str, chat_session_request: ChatSessionRequest, user_id: str
    ) -> Tuple[Optional[ChatSession], Optional[APIError]]:
        """
        Update chat session.

        Args:
            chat_session_id(str): Chat session id
            chat_session_request(ChatSessionRequest): Chat session request object
            user_id(str): User id

        Returns:
            Tuple[Optional[ChatSession], Optional[APIError]]: Chat session object and APIError object if any error
        """
        with self._transaction():
            # Define to-be-updated chat session
            chat_session = chat_session_request.model_dump(exclude_unset=True)

            # Update chat session
            err = self._chat_repository.update_chat_session(
                chat_session_id=chat_session_id, chat_session=chat_session, user_id=user_id
            )
            if err:
                return err

        # Get the updated chat session
        return self._chat_repository.get_chat_session(
            chat_session_id=chat_session_id, user_id=user_id
        )

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
            parent_updated_message = ChatMessageRequest(
                child_message_id=child_message_id
            ).model_dump(exclude_unset=True)
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
            child_updated_message = ChatMessageRequest(
                parent_message_id=parent_message_id
            ).model_dump(exclude_unset=True)
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
    ) -> Tuple[Optional[ChatMessage], Optional[APIError]]:
        """
        Make chat request message.

        Args:
            user_id(str): User id
            chat_session_id(str): Chat session id
            message(str): Message text
            message_type(ChatMessageType): Message type
            latest_chat_response(ChatMessage): Latest chat response message. Defaults to None

        Returns:
            Tuple[Optional[ChatMessage], Optional[APIError]]: Chat request message and APIError object if any error
        """
        # Define the parent message id as the latest chat response id (if any)
        parent_message_id = latest_chat_response.id if latest_chat_response else None

        # Create chat request message
        new_chat_request = ChatMessage(
            chat_session_id=chat_session_id,
            parent_message_id=parent_message_id,
            message=message,
            message_type=message_type,
        )

        # Create chat request message
        logger.info("Creating a new chat request message")
        err = self._chat_repository.create_chat_message(chat_message=new_chat_request)
        if err:
            return None, err

        # Flush the session to send the data to the database (but do not commit yet)
        self._db_session.flush()

        # Update the child_message_id of the latest chat response (if any)
        if latest_chat_response:
            logger.info("Updating the child_message_id of the latest chat response message")
            latest_updated_chat_response = ChatMessageRequest(
                child_message_id=new_chat_request.id
            ).model_dump(exclude_unset=True)
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
        current_request_id: str,
    ) -> Generator[str, None, Tuple[Optional[ChatMessage], Optional[APIError]]]:
        """
        Generate a streaming chat response message.
        Uses the input message to query the LLM model and generate a streaming response message.

        Args:
            chat_message_request (ChatMessageRequest): Chat message request object.
            chat_session_id (str): Chat session ID.
            current_request_id (str): Current request message ID.

        Yields:
            str: A chunk of the response message generated by the LLM model.

        Returns:
            Tuple[Optional[ChatMessage], Optional[APIError]]: The final chat response message and an APIError object if an error occurs.
        """
        try:
            # TODO: Replace by own LLM retrieval process
            # Initialize OpenAI client
            client = openai.OpenAI()

            # Initialize empty response message
            accumulated_response = []

            # Generate chat response
            # TODO: Replace this step by own LLM generation process
            response: Generator[ChatCompletionChunk, None, None] = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": chat_message_request.message}],
                stream=True,
                max_tokens=1000,
            )

            # Stream each chunk as it arrives
            for chunk in response:
                if content := getattr(chunk.choices[0].delta, "content", None):
                    accumulated_response.append(content)
                    yield content

            # Create final response message with complete text
            if not accumulated_response:
                logger.warning(f"No content received from LLM for session {chat_session_id}")
                return None, APIError(kind=ErrorCodesMappingNumber.NO_CONTENT.value)

            # Create final response message with complete text
            complete_response = "".join(accumulated_response)
            chat_response = ChatMessage(
                chat_session_id=chat_session_id,
                parent_message_id=current_request_id,
                message=complete_response,
                message_type=ChatMessageType.ASSISTANT,
            )

            # Store the complete message in the database
            logger.info("Creating a new chat response message")
            if err := self._chat_repository.create_chat_message(chat_message=chat_response):
                return None, err

            # Flush the session to send the data to the database (but do not commit yet)
            self._db_session.flush()

            return chat_response, None

        except Exception as e:
            logger.error(
                f"Error generating chat response - Session: {chat_session_id}, Request: {current_request_id}, Error: {e}"
            )
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

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
            Tuple[Optional[ChatMessage], Optional[APIError]]: New chat message object and APIError object if any error
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

        return current_chat_request, None

    def _handle_new_chat_message(
        self, chat_message_request: ChatMessageRequest, chat_session_id: str, user_id: str
    ) -> Generator[
        str, None, Tuple[Optional[ChatMessage], Optional[ChatMessage], Optional[APIError]]
    ]:
        """
        Handle a new chat message in the chat session with streaming support.

        Args:
            chat_message_request (ChatMessageRequest): Chat message request object.
            chat_session_id (str): Chat session ID.
            user_id (str): User ID.

        Yields:
            str: A chunk of the response message generated by the LLM model.

        Returns:
            Tuple[Optional[ChatMessage], Optional[ChatMessage], Optional[APIError]]:
            A tuple containing (chat_response, chat_request, error).
            - chat_response: The final chat response message
            - chat_request: The chat request message
            - error: An error object if an error occurs
        """
        try:
            # Get the current chat messages in the chat session
            current_chat_messages, err = self._chat_repository.get_chat_messages(
                chat_session_id=chat_session_id, user_id=user_id
            )
            if err:
                return None, None, err

            # If there are no chat messages, the request message is the first message in the chat session
            latest_chat_response = current_chat_messages[-1] if current_chat_messages else None

            # Create chat request message. The request message is the user message
            chat_request, err = self._make_chat_request(
                user_id=user_id,
                chat_session_id=chat_session_id,
                message=chat_message_request.message,
                message_type=ChatMessageType.USER,
                latest_chat_response=latest_chat_response,
            )
            if err:
                return None, None, err

            # Generate and stream chat response
            response_generator = self._generate_chat_response(
                chat_message_request=chat_message_request,
                chat_session_id=chat_session_id,
                current_request_id=chat_request.id,
            )

            # Accumulate the response chunks
            chat_response = None
            try:
                while True:
                    # Stream each chunk of the response
                    yield next(response_generator)
            except StopIteration as e:
                if e.value is not None:
                    chat_response, err = e.value
                    if err:
                        return None, None, err

            # Finalize the generator to retrieve the complete response
            try:
                # Update child_message_id of the request message
                updated_message = ChatMessageRequest(child_message_id=chat_response.id).model_dump(
                    exclude_unset=True
                )
                if err := self._chat_repository.update_chat_message(
                    chat_session_id=chat_session_id,
                    chat_message_id=chat_request.id,
                    chat_message=updated_message,
                    user_id=user_id,
                ):
                    return None, None, err

                return chat_response, chat_request, None

            except StopIteration as e:
                if e.value is not None:
                    chat_response, err = e.value
                    return chat_response, chat_request, err

                return (
                    None,
                    None,
                    APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value),
                )

        except Exception as e:
            logger.error(f"Error handling new chat message: {str(e)}")
            return None, APIError(kind=ErrorCodesMappingNumber.INTERNAL_SERVER_ERROR.value)

    def generate_stream_chat_message(
        self, chat_message_request: ChatMessageRequest, chat_session_id: str, user_id: str
    ) -> Generator[Tuple[str, str], None, None]:
        """
        Generate a streaming chat message for the new message request.

        Args:
            chat_message_request (ChatMessageRequest): Chat message request object.
            chat_session_id (str): Chat session ID.
            user_id (str): User ID.

        Yields:
            Tuple[str, str]: A tuple containing the user message and a chunk of the response message.
        """
        with self._transaction():
            chat_session, err = self._chat_repository.get_chat_session(
                chat_session_id=chat_session_id, user_id=user_id
            )
            if err or not chat_session:
                yield ChatStreamResponse(
                    content=f"Chat session not found: {err}", type=ChatStreamType.ERROR
                ).as_str()
                return

            # Handle request types
            # if chat_message_request.request_type == ChatMessageRequestType.REGENERATE:
            #     logger.info("Regenerating the existing chat message")
            #     existing_chat_request, err = self._handle_existing_chat_message(
            #         chat_message_request=chat_message_request,
            #         chat_session_id=chat_session_id,
            #         user_id=user_id,
            #     )
            #     if err:
            #         yield json.dumps(
            #             {"c": f"Error during regeneration: {err}", "t": ChatStreamType.ERROR}
            #         )
            #         return
            #     chat_message_request.message = existing_chat_request.message

            # elif chat_message_request.request_type == ChatMessageRequestType.EDIT:
            #     logger.info("Editing the existing chat message")
            #     _, err = self._handle_existing_chat_message(
            #         chat_message_request=chat_message_request,
            #         chat_session_id=chat_session_id,
            #         user_id=user_id,
            #     )
            #     if err:
            #         yield json.dumps(
            #             {"c": f"Error during editing: {err}", "t": ChatStreamType.ERROR}
            #         )
            #         return
            if chat_message_request.request_type in (
                ChatMessageRequestType.REGENERATE,
                ChatMessageRequestType.EDIT,
            ):
                action = (
                    "Regenerating"
                    if chat_message_request.request_type == ChatMessageRequestType.REGENERATE
                    else "Editing"
                )
                logger.info(f"{action} the existing chat message")

                # Handle existing chat message
                existing_chat_request, err = self._handle_existing_chat_message(
                    chat_message_request=chat_message_request,
                    chat_session_id=chat_session_id,
                    user_id=user_id,
                )
                if err:
                    yield ChatStreamResponse(
                        content=f"Error during {action.lower()}: {err}", type=ChatStreamType.ERROR
                    ).as_str()
                    return

                if chat_message_request.request_type == ChatMessageRequestType.REGENERATE:
                    chat_message_request.message = existing_chat_request.message

            logger.info("Handling new chat message")

            # Handle new message streaming
            response_generator = self._handle_new_chat_message(
                chat_message_request=chat_message_request,
                chat_session_id=chat_session_id,
                user_id=user_id,
            )

            chat_request: ChatMessage = None
            chat_response: ChatMessage = None
            buffer = []
            try:
                # Process the generator to get sequences of response's chunks
                while True:
                    buffer.append(next(response_generator))
            except StopIteration as e:
                if e.value is not None:
                    chat_response, chat_request, err = e.value
                    if err:
                        yield ChatStreamResponse(
                            content=f"Error during request generation: {err}",
                            type=ChatStreamType.ERROR,
                        ).as_str()
                        return
                else:
                    yield ChatStreamResponse(
                        content="Unexpected end of request generation", type=ChatStreamType.ERROR
                    ).as_str()
                    return

            # Stream the request first
            yield ChatStreamResponse(
                content=ChatMessageResponse.model_validate(chat_request).model_dump(),
                type=ChatStreamType.REQUEST,
            ).as_str()

            # Stream the response's content in chunks
            for chunk in buffer:
                yield ChatStreamResponse(content=chunk, type=ChatStreamType.CHUNK).as_str()

            # Stream the response finally
            yield ChatStreamResponse(
                content=ChatMessageResponse.model_validate(chat_response).model_dump(),
                type=ChatStreamType.DONE,
            ).as_str()

    def create_chat_feedback(
        self, chat_feedback_request: ChatFeedbackRequest
    ) -> Optional[APIError]:
        """
        Create chat feedback.

        Args:
            chat_feedback_request: ChatFeedbackRequest

        Returns:
            Optional[APIError]: APIError object if any error
        """
        with self._transaction():
            # Define chat feedback
            chat_feedback = ChatFeedback(
                chat_message_id=chat_feedback_request.chat_message_id,
                is_positive=chat_feedback_request.is_positive,
                feedback_text=chat_feedback_request.feedback_text,
            )

            # Create chat feedback
            err = self._chat_feedback_repository.create_chat_feedback(chat_feedback=chat_feedback)

        return err if err else None
