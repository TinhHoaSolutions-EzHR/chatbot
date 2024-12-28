from typing import Optional

import tiktoken
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.openai import OpenAIEmbeddingMode
from llama_index.embeddings.voyageai import VoyageEmbedding
from llama_index.llms.openai import OpenAI

from app.models.embedding import EmbeddingProviderType
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


def handle_current_embedding_model(
    embedding_model_name: str,
    embedding_type: EmbeddingProviderType,
    batch_size: int,
    dimensions: int,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    callback_manager: Optional[CallbackManager] = None,
) -> None:
    """
    Handle the current embedding model based on the embedding type.

    Args:
        embedding_model_name (str): Name of the embedding model.
        embedding_type (EmbeddingProviderType): Type of the embedding provider.
        batch_size (int): Batch size for embedding.
        dimensions (int): Dimensions for the embedding.
        api_key (Optional[str], optional): API key for the embedding provider. Defaults to None.
        api_base (Optional[str], optional): API base for the embedding provider. Defaults to None.
        callback_manager (Optional[CallbackManager], optional): Manager for handling callbacks. Defaults to None.
    """
    try:
        if embedding_type == EmbeddingProviderType.OPENAI:
            Settings.embed_model = OpenAIEmbedding(
                mode=OpenAIEmbeddingMode.TEXT_SEARCH_MODE,
                model=embedding_model_name,
                embed_batch_size=batch_size,
                dimensions=dimensions,
                api_key=api_key,
                api_base=api_base,
                callback_manager=callback_manager,
            )
        elif embedding_type == EmbeddingProviderType.GEMINI:
            Settings.embed_model = GeminiEmbedding(
                model_name=embedding_model_name,
                embed_batch_size=batch_size,
                api_key=api_key,
                api_base=api_base,
                callback_manager=callback_manager,
            )
        elif embedding_type == EmbeddingProviderType.COHERE:
            Settings.embed_model = CohereEmbedding(
                model_name=embedding_model_name,
                embed_batch_size=batch_size,
                api_key=api_key,
                base_url=api_base,
                callback_manager=callback_manager,
            )
        elif embedding_type == EmbeddingProviderType.VOYAGE:
            Settings.embed_model = VoyageEmbedding(
                model_name=embedding_model_name,
                embed_batch_size=batch_size,
                output_dimension=dimensions,
                voyage_api_key=api_key,
                callback_manager=callback_manager,
            )
        elif embedding_type == EmbeddingProviderType.AZURE_OPENAI:
            Settings.embed_model = AzureOpenAIEmbedding(
                model_name=embedding_model_name,
                embed_batch_size=batch_size,
                api_key=api_key,
                api_base=api_base,
                callback_manager=callback_manager,
            )
        else:
            raise ValueError(f"Invalid embedding provider type: {embedding_type}")
    except Exception as e:
        raise ValueError(f"Error setting the current embedding model: {e}")
