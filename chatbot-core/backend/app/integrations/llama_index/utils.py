from typing import List

from llama_index.core.base.llms.types import MessageRole
from llama_index.core.types import ChatMessage as LlamaIndexChatMessage

from app.models import ChatMessage
from app.models.chat import ChatMessageType


def llamaify_messages(
    chat_messages: List[ChatMessage],
) -> List[LlamaIndexChatMessage]:
    """
    Convert application ChatMessage objects to LlamaIndex ChatMessage objects.

    Args:
        chat_messages: List of application ChatMessage objects to convert.

    Returns:
        A list of converted LlamaIndex ChatMessage objects with mapped roles
        and original message content.
    """
    message_type_mapping = {
        ChatMessageType.USER: MessageRole.USER,
        ChatMessageType.ASSISTANT: MessageRole.ASSISTANT,
    }

    return [
        LlamaIndexChatMessage(
            role=message_type_mapping[chat_message.message_type],
            content=chat_message.message or "",
        )
        for chat_message in chat_messages
    ]
