import asyncio
from collections.abc import AsyncGenerator
from typing import List
from typing import Optional
from typing import Tuple

from llama_index.core import Settings
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.types import ChatMessage as LlamaIndexChatMessage
from sqlalchemy.orm import Session

from app.databases.qdrant import QdrantConnector
from app.integrations.llama_index.utils import llamaify_messages
from app.models import ChatFeedback
from app.models import ChatMessage
from app.models import ChatSession
from app.models.chat import ChatFeedbackRequest
from app.models.chat import ChatMessageRequest
from app.models.chat import ChatMessageRequestType
from app.models.chat import ChatMessageResponse
from app.models.chat import ChatMessageStreamEventType
from app.models.chat import ChatMessageType
from app.models.chat import ChatSessionRequest
from app.models.chat import ChatStreamResponse
from app.repositories.chat import ChatRepository
from app.services.base import BaseService
from app.settings import Constants
from app.utils.api.api_response import APIError
from app.utils.api.error_handler import ConversationError
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class ChatService(BaseService):
    def __init__(self, db_session: Session, qdrant_connector: Optional[QdrantConnector] = None):
        """
        Chat service class for handling chat-related operations.

        Args:
            db_session(Session): Database session
            qdrant_connector(QdrantConnector): Vector database connection. Defaults to None.
        """
        super().__init__(db_session=db_session)

        # Define repositories
        self._chat_repository = ChatRepository(db_session=self._db_session)

        # Define external storage's connectors
        self._qdrant_connector = qdrant_connector

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

    async def _generate_chat_response(
        self,
        chat_message_request: ChatMessageRequest,
        chat_session_id: str,
        current_request_id: str,
        pre_register_chat_response: ChatMessage,
        chat_history: List[LlamaIndexChatMessage],
    ) -> AsyncGenerator[str, None, None]:
        """
        Generate a streaming chat response message.
        Uses the input message to query the LLM model and generate a streaming response message.

        Args:
            chat_message_request (ChatMessageRequest): Chat message request object.
            chat_session_id (str): Chat session ID.
            current_request_id (str): Current request message ID.
            pre_register_chat_response (ChatMessage): Pre-registered chat response message.
            chat_history (List[LlamaIndexChatMessage]): The LlamaIndex chat history of the chat session.

        Yields:
            str: A chunk of the response message generated by the LLM model.
        """
        try:
            # Convert chat history to LlamaIndex chat messages
            chat_history = llamaify_messages(chat_messages=chat_history)

            # TODO: Remove it as this is just a workaround solution
            # from app.main import index

            # Define retriever
            # vector_params = VectorParams(
            #     size=Constants.DIMENSIONS, distance=Constants.DISTANCE_METRIC_TYPE
            # )
            # vector_store = QdrantVectorStore(
            #     collection_name=Constants.QDRANT_COLLECTION,
            #     client=self._qdrant_connector.get_client(),
            #     aclient=self._qdrant_connector.get_aclient(),
            #     dense_config=vector_params,
            # )
            # index: VectorStoreIndex = VectorStoreIndex.from_vector_store(vector_store=vector_store)
            from app.main import index

            retriever = index.as_retriever(similarity_top_k=Constants.SIMILARITY_TOP_K)

            # chat_engine = index.as_chat_engine()
            # Define chat engine
            chat_engine = CondensePlusContextChatEngine.from_defaults(
                retriever=retriever,
                chat_history=chat_history,
                system_prompt=Constants.CHAT_ENGINE_SYSTEM_PROMPT,
                context_prompt=Constants.CHAT_ENGINE_CONTEXT_PROMPT,
                context_refine_prompt=Constants.CHAT_ENGINE_CONTEXT_PROMPT,
                condense_prompt=Constants.CHAT_ENGINE_CONDENSE_PROMPT,
                verbose=True,
            )

            response_streaming = await chat_engine.astream_chat(
                message=chat_message_request.message,
            )

            # Initialize empty response message
            accumulated_response = []

            # Stream each chunk as it arrives
            try:
                async for chunk in response_streaming.async_response_gen():
                    accumulated_response.append(chunk)
                    yield ChatStreamResponse(
                        event=ChatMessageStreamEventType.DELTA, content=chunk
                    ).as_json()
            except asyncio.CancelledError:
                logger.warning(
                    f"Client disconnected - Chat session: {chat_session_id}, Chat request: {current_request_id}"
                )
            except Exception as e:
                logger.error(
                    f"Error streaming chat response - Chat session: {chat_session_id}, Chat request: {current_request_id}, Error: {e}"
                )
                yield ChatStreamResponse(
                    event=ChatMessageStreamEventType.ERROR,
                    content=f"Error streaming chat response: {e}",
                ).as_json()

            # Create final response message with complete text
            if not accumulated_response:
                logger.warning(
                    f"No content received from agent for session {chat_session_id} for request {current_request_id}"
                )
                yield ChatStreamResponse(
                    event=ChatMessageStreamEventType.ERROR,
                    content="No content received from agent",
                ).as_json()

            # Create final response message with complete text
            complete_response = "".join(accumulated_response) if accumulated_response else ""
            pre_register_chat_response.message = complete_response

            # Store the complete message in the database
            logger.info("Creating a new chat response message")
            if err := self._chat_repository.create_chat_message(
                chat_message=pre_register_chat_response
            ):
                yield ChatStreamResponse(
                    event=ChatMessageStreamEventType.ERROR,
                    content=f"Error during response creation: {err}",
                ).as_json()

            # Flush the session to send the data to the database (but do not commit yet)
            self._db_session.flush()
        except Exception as e:
            logger.error(
                f"Error generating chat response - Chat session: {chat_session_id}, Chat request: {current_request_id}, Error: {e}",
                exc_info=True,
            )
            yield ChatStreamResponse(
                event=ChatMessageStreamEventType.ERROR,
                content=f"Error generating chat response: {e}",
            ).as_json()

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

    async def _handle_naming_chat_session(
        self,
        chat_session_id: str,
        user_id: str,
        chat_request_message: str = "",
        chat_response_message: str = "",
    ) -> AsyncGenerator[str, None, None]:
        """
        Handle naming chat session.

        Args:
            chat_session_id(str): Chat session id
            user_id(str): User id
            chat_request_message(str): Chat request message. Defaults to "".
            chat_response_message(str): Chat response message. Defaults to "".

        Returns:
            AsyncGenerator[str, None, None]: Async generator of chat session naming response.
        """
        # Construct prompt
        prompt = Constants.CHAT_SESSION_NAMING_PROMPT.format(
            user_message=chat_request_message, agent_message=chat_response_message
        )

        # Generate a name for the chat session
        session_name_response = await Settings.llm.acomplete(prompt=prompt)
        session_name = session_name_response.text.strip() or "Untitled Chat"
        yield ChatStreamResponse(
            event=ChatMessageStreamEventType.TITLE_GENERATION, content=session_name
        ).as_json()

        # Rename the chat session with the generated name
        updated_chat_session = ChatSessionRequest(description=session_name).model_dump(
            exclude_unset=True
        )
        if err := self._chat_repository.update_chat_session(
            chat_session_id=chat_session_id, chat_session=updated_chat_session, user_id=user_id
        ):
            yield ChatStreamResponse(
                event=ChatMessageStreamEventType.ERROR,
                content=f"Error during chat session naming: {err}",
            ).as_json()

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

    async def _handle_new_chat_message(
        self,
        chat_message_request: ChatMessageRequest,
        chat_session: ChatSession,
        chat_session_id: str,
        user_id: str,
    ) -> AsyncGenerator[str, None, None]:
        """
        Handle a new chat message in the chat session with streaming support.

        Args:
            chat_message_request (ChatMessageRequest): Chat message request object.
            chat_session (ChatSession): Chat session object.
            chat_session_id (str): Chat session ID.
            user_id (str): User ID.

        Yields:
            str: A chunk of the response message generated by the LLM model.
        """
        try:
            # Get the current chat messages in the chat session
            chat_history = chat_session.chat_messages

            # If there are no chat messages, the request message is the first message in the chat session
            latest_chat_response = chat_history[-1] if chat_history else None

            # Create chat request message. The request message is the user message
            chat_request, err = self._make_chat_request(
                user_id=user_id,
                chat_session_id=chat_session_id,
                message=chat_message_request.message,
                message_type=ChatMessageType.USER,
                latest_chat_response=latest_chat_response,
            )
            if err:
                yield ChatStreamResponse(
                    event=ChatMessageStreamEventType.ERROR,
                    content=f"Error during request creation: {err}",
                ).as_json()

            # Pre-register and create a new chat response message
            chat_response = ChatMessage(
                chat_session_id=chat_session_id,
                message="",
                message_type=ChatMessageType.ASSISTANT,
            )
            if err := self._chat_repository.create_chat_message(chat_message=chat_response):
                yield ChatStreamResponse(
                    event=ChatMessageStreamEventType.ERROR,
                    content=f"Error during response creation: {err}",
                ).as_json()

            # Flush the session to send the data to the database (but do not commit yet)
            self._db_session.flush()

            # Update child_message_id of the request message and parent_message_id of the response message
            chat_request.child_message_id = chat_response.id
            chat_response.parent_message_id = chat_request.id

            # Flush the session to send the data to the database (but do not commit yet)
            self._db_session.flush()

            # Stream the chat request message object
            yield ChatStreamResponse(
                event=ChatMessageStreamEventType.METADATA,
                content=ChatMessageResponse.model_validate(chat_request).model_dump(mode="json"),
            ).as_json()

            # Generate and stream chat response message in chunks
            async for chunk in self._generate_chat_response(
                chat_message_request=chat_message_request,
                chat_session_id=chat_session_id,
                current_request_id=chat_request.id,
                pre_register_chat_response=chat_response,
                chat_history=chat_history,
            ):
                yield chunk

            # Name chat session if it is newly created
            if (
                chat_request.parent_message_id is None
                and chat_message_request.request_type == ChatMessageRequestType.NEW
            ):
                logger.info("Chat session is newly created. Naming the chat session...")
                async for chunk in self._handle_naming_chat_session(
                    chat_session_id=chat_session_id,
                    user_id=user_id,
                    chat_request_message=chat_request.message,
                    chat_response_message=chat_response.message,
                ):
                    yield chunk

            # Stream the chat response message object. We don't include the message content in the response.
            yield ChatStreamResponse(
                event=ChatMessageStreamEventType.STREAM_COMPLETE,
                content=ChatMessageResponse.model_validate(chat_response).model_dump(
                    mode="json", exclude={"message"}
                ),
            ).as_json()

        except Exception as e:
            logger.error(f"Error handling new chat message: {e}")
            yield ChatStreamResponse(
                event=ChatMessageStreamEventType.ERROR,
                content=f"Error handling new chat message: {e}",
            ).as_json()

    def _handle_regenerate_or_edit_chat_message(
        self, chat_message_request: ChatMessageRequest, chat_session_id: str, user_id: str
    ) -> Optional[APIError]:
        """
        Handle the regenerate or edit chat message request.

        Args:
            chat_message_request (ChatMessageRequest): Chat message request object.
            chat_session_id (str): Chat session ID.
            user_id (str): User ID.

        Returns:
            Optional[APIError]: APIError object if any error.
        """
        if chat_message_request.request_type not in (
            ChatMessageRequestType.REGENERATE,
            ChatMessageRequestType.EDIT,
        ):
            return None

        action = (
            "Regenerating"
            if chat_message_request.request_type == ChatMessageRequestType.REGENERATE
            else "Editing"
        )
        logger.info(f"{action} the existing chat message")

        existing_chat_request, err = self._handle_existing_chat_message(
            chat_message_request=chat_message_request,
            chat_session_id=chat_session_id,
            user_id=user_id,
        )
        if err:
            return err

        if chat_message_request.request_type == ChatMessageRequestType.REGENERATE:
            chat_message_request.message = existing_chat_request.message

        return None

    async def generate_stream_chat_message(
        self,
        chat_message_request: ChatMessageRequest,
        chat_session_id: str,
        user_id: str,
    ) -> AsyncGenerator[str, None, None]:
        """
        Generate a streaming chat message for the new message request.

        Args:
            chat_message_request (ChatMessageRequest): Chat message request object.
            chat_session_id (str): Chat session ID.
            user_id (str): User ID.

        Yields:
            str: A chunk of the response message generated by the LLM model.
        """
        with self._transaction():
            chat_session, err = self._chat_repository.get_chat_session(
                chat_session_id=chat_session_id, user_id=user_id
            )
            if err or not chat_session:
                yield ChatStreamResponse(
                    event=ChatMessageStreamEventType.ERROR,
                    content=f"Chat session not found: {err}",
                ).as_json()
                return

            # Handle regenerated or edited chat message
            err = self._handle_regenerate_or_edit_chat_message(
                chat_message_request=chat_message_request,
                chat_session_id=chat_session_id,
                user_id=user_id,
            )
            if err:
                yield ChatStreamResponse(
                    event=ChatMessageStreamEventType.ERROR,
                    content=f"Error during request handling: {err}",
                ).as_json()
                return

            logger.info("Handling new chat message")

            # Handle new streaming response message
            async for chunk in self._handle_new_chat_message(
                chat_message_request=chat_message_request,
                chat_session=chat_session,
                chat_session_id=chat_session_id,
                user_id=user_id,
            ):
                yield chunk

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
