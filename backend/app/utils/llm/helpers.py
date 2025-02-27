import os
from logging import Logger
from typing import Optional

import tiktoken
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.openai import OpenAIEmbeddingMode
from llama_index.llms.cohere import Cohere
from llama_index.llms.gemini import Gemini
from llama_index.llms.openai import OpenAI
from openai import APIStatusError
from openai import OpenAIError
from tenacity import retry
from tenacity import stop_after_attempt

from app.models.provider import ProviderType
from app.settings import Constants
from app.settings import Secrets


@retry(stop=stop_after_attempt(Constants.RETRY_TIMES))
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
    api_key = get_openai_api_key()

    # Set the tokenizer for model
    Settings.tokenizer = tiktoken.encoding_for_model(model_name=llm_model).encode

    # INFO: Try to create request to OpenAI to check it is working
    # If this works, that means the below embedding model will work
    llm_client = OpenAI(
        api_key=api_key,
        model=llm_model,
        temperature=0.3,
        callback_manager=callback_manager,
    )
    try:
        llm_client.complete("Hello, world!")
    except OpenAIError as e:
        raise ValueError(f"There're something wrong with the API key: {e}")
    except APIStatusError as e:
        raise ValueError(f"Failed to create LLM with OpenAI client: {e}")

    # Set the LLM model with specified parameters
    # TODO: add support for other LLM providers
    Settings.llm = llm_client

    # Set the embedding model with specified parameters
    # TODO: add support for other embedding providers
    embedding_client = OpenAIEmbedding(
        api_key=api_key,
        mode=OpenAIEmbeddingMode.SIMILARITY_MODE,
        model=embedding_model,
        embed_batch_size=Constants.EMBEDDING_BATCH_SIZE,
        dimensions=Constants.DIMENSIONS,
        callback_manager=callback_manager,
    )
    Settings.embed_model = embedding_client

    Settings.num_output = Constants.LLM_MAX_OUTPUT_LENGTH
    Settings.context_window = Constants.LLM_MAX_CONTEXT_WINDOW
    Settings.callback_manager = callback_manager


def get_openai_api_key() -> str:
    """
    Get the OpenAI API key specified in the environment variables.

    Returns:
        str: OpenAI API key

    Raises:
        ValueError: OpenAI API key not found.
    """
    api_key = os.getenv("OPENAI_API_KEY") or Secrets.LLM_API_KEY
    if not api_key:
        raise ValueError("OpenAI API key not found.")
    return api_key


def handle_current_llm_model(
    llm_model_name: str,
    provider_type: ProviderType,
    temperature: float = 0.7,
    api_key: Optional[str] = None,
    callback_manager: Optional[CallbackManager] = None,
    logger: Optional[Logger] = None,
) -> None:
    """
    Handle the current LLM model.

    Args:
        llm_model_name (str): Name of the LLM model.
        provider_type (ProviderType): Type of the LLM provider.
        temperature (float): Temperature for the LLM model. Defaults to 0.7.
        api_key (Optional[str]): API key for the LLM model. Defaults to None.
        callback_manager (Optional[CallbackManager]): Manager for handling callbacks. Defaults to None.
        logger (Optional[Logger]): Logger for logging. Defaults to None.
    """
    if logger:
        logger.info(f"Setting the current LLM model: {llm_model_name} for {provider_type}")

    try:
        # Set the LLM model based on the provider type
        if provider_type == ProviderType.OPENAI:
            Settings.llm = OpenAI(
                model=llm_model_name,
                temperature=temperature,
                api_key=api_key,
                callback_manager=callback_manager,
            )

            # Set the tokenizer for the llm model
            Settings.tokenizer = tiktoken.encoding_for_model(model_name=llm_model_name).encode
        elif provider_type == ProviderType.GEMINI:
            Settings.llm = Gemini(
                model=llm_model_name,
                temperature=temperature,
                api_key=api_key,
                callback_manager=callback_manager,
            )

            # Set the tokenizer to None for Gemini
            Settings.tokenizer = None
        elif provider_type == ProviderType.COHERE:
            Settings.llm = Cohere(
                model=llm_model_name,
                temperature=temperature,
                api_key=api_key,
                callback_manager=callback_manager,
            )

            # Set the tokenizer to None for Cohere
            Settings.tokenizer = None
        else:
            raise ValueError(f"Invalid LLM provider type: {llm_model_name}")
    except Exception as e:
        raise ValueError(f"Error setting the current LLM model: {e}")


def handle_current_embedding_model(
    embedding_model_name: str,
    provider_type: ProviderType,
    batch_size: int,
    dimensions: int,
    api_key: Optional[str] = None,
    callback_manager: Optional[CallbackManager] = None,
    logger: Optional[Logger] = None,
) -> None:
    """
    Handle the current embedding model based on the embedding type.

    Args:
        embedding_model_name (str): Name of the embedding model.
        provider_type (ProviderType): Type of the embedding provider.
        batch_size (int): Batch size for embedding.
        dimensions (int): Dimensions for the embedding.
        api_key (Optional[str]): API key for the embedding provider. Defaults to None.
        callback_manager (Optional[CallbackManager]): Manager for handling callbacks. Defaults to None.
        logger (Optional[Logger]): Logger for logging. Defaults to None.
    """
    if logger:
        logger.info(
            f"Setting the current embedding model: {embedding_model_name} for {provider_type}"
        )

    try:
        # Set the embedding model based on the provider type
        if provider_type == ProviderType.OPENAI:
            Settings.embed_model = OpenAIEmbedding(
                mode=OpenAIEmbeddingMode.TEXT_SEARCH_MODE,
                model=embedding_model_name,
                embed_batch_size=batch_size,
                dimensions=dimensions,
                api_key=api_key,
                callback_manager=callback_manager,
            )
        elif provider_type == ProviderType.GEMINI:
            Settings.embed_model = GeminiEmbedding(
                model_name=embedding_model_name,
                embed_batch_size=batch_size,
                api_key=api_key,
                callback_manager=callback_manager,
            )
        elif provider_type == ProviderType.COHERE:
            Settings.embed_model = CohereEmbedding(
                model_name=embedding_model_name,
                embed_batch_size=batch_size,
                api_key=api_key,
                callback_manager=callback_manager,
            )
        else:
            raise ValueError(f"Invalid embedding provider type: {provider_type}")
    except Exception as e:
        raise ValueError(f"Error setting the current embedding model: {e}")
