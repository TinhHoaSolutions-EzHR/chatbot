from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from app.settings import Constants


def init_llamaindex_config(
    llm_model: str = Constants.OPENAI_LLM_MODEL,
    embedding_model: str = Constants.OPENAI_EMBEDDING_MODEL,
) -> None:
    """
    Initialize the LlamaIndex configuration

    Args:
        llm_model (str, optional): LLM model. Defaults to "gpt-4o-mini".
        embedding_model (str, optional): Embedding model. Defaults to "text-embedding-3-small".
    """
    # Define LLamaIndex settings
    Settings.llm = OpenAI(model=llm_model)
    Settings.embed_model = OpenAIEmbedding(model=embedding_model)
