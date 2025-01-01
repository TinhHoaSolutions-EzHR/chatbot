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

from app.models.provider import ProviderType
from app.settings import Constants


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
