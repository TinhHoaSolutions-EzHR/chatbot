import os

import tiktoken

from app.settings import Constants
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.openai import OpenAIEmbeddingMode
from llama_index.llms.openai import OpenAI


def init_llm_configurations(
    llm_model: str,
    embedding_model: str,
    callback_manager: CallbackManager | None = None,
) -> None:
    """
    Initialize the LlamaIndex configuration

    Args:
        llm_model (str, optional): LLM model. Defaults to "gpt-4o-mini".
        embedding_model (str, optional): Embedding model. Defaults to "text-embedding-3-small".
        callback_manager (CallbackManager, optional): Manager for handling callbacks. Defaults to None.
    """
    # Set the tokenizer for model
    Settings.tokenizer = tiktoken.encoding_for_model(model_name=llm_model).encode

    # Set the LLM model with specified parameters
    Settings.llm = OpenAI(model=llm_model, temperature=0, callback_manager=callback_manager)

    # Set the embedding model with specified parameters
    Settings.embed_model = OpenAIEmbedding(
        mode=OpenAIEmbeddingMode.TEXT_SEARCH_MODE,
        model=embedding_model,
        embed_batch_size=Constants.EMBEDDING_BATCH_SIZE,
        dimensions=Constants.DIMENSIONS,
        callback_manager=callback_manager,
    )
    Settings.num_output = Constants.LLM_MAX_OUTPUT_LENGTH
    Settings.context_window = Constants.LLM_MAX_CONTEXT_WINDOW
    Settings.callback_manager = callback_manager


def get_openai_api_key() -> str:
    """
    Get the OpenAI API key

    Returns:
        str: OpenAI API key
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OpenAI API key not found")
    return os.getenv("OPENAI_API_KEY")
