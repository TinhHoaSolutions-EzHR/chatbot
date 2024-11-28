from fastapi import File, UploadFile
from llama_index.core import Settings
from llama_index.core.extractors import KeywordExtractor, QuestionsAnsweredExtractor
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import BaseNode
from llama_index.vector_stores.qdrant import QdrantVectorStore
from typing import Annotated, Any, List

from app.databases.qdrant import get_vector_db_client
from app.databases.redis import get_cache_store_client
from app.settings import Constants
from app.utils.pdf_reader import parse_pdf


def get_transformations() -> List[Any]:
    """
    Get the transformation components for the ingestion pipeline
    """
    # Define node postprocessor methods
    extractors = [
        QuestionsAnsweredExtractor(llm=Settings.llm, questions=2),
        KeywordExtractor(llm=Settings.llm, keywords=5),
    ]

    # Define chunking method
    semantic_splitter = SemanticSplitterNodeParser(
        buffer_size=1,
        breakpoint_percentile_threshold=95,
        embed_model=Settings.embed_model,
    )

    transformations = [semantic_splitter] + extractors

    return transformations


def index_document_to_vector_db(
    file: Annotated[UploadFile, File(description="PDF file")],
) -> None:
    # Parse PDF file into LlamaIndex Document objects
    documents = parse_pdf(file)

    # Define vector store
    vector_db_client = get_vector_db_client()
    vector_store = QdrantVectorStore(
        client=vector_db_client,
        collection_name=Constants.LLM_QDRANT_COLLECTION,
    )

    # Initialize the cache store for the ingestion pipeline
    cache = get_cache_store_client()
    ingest_cache = IngestionCache(
        cache=cache,
        collection=Constants.LLM_REDIS_CACHE_COLLECTION,
    )

    # Define transformation components (chunking + node postprocessors)
    transformations = get_transformations()

    # Ingestion pipeline to vector database
    pipeline = IngestionPipeline(
        name="EzHR Chatbot Indexing Pipeline",
        transformations=transformations,
        # TODO: Remove this parameter after finishing the development
        # vector_store=vector_store,
        cache=ingest_cache,
        # TODO: Remove this parameter after finishing the development
        disable_cache=True,
    )
    nodes: List[BaseNode] = pipeline.run(documents=documents, show_progress=True)

    # TODO: Will be deleted after figuring out why vector embeddings
    # are not being stored in the Qdrant database when calling IngestionPipeline.run()
    for node in nodes:
        node_embedding = Settings.embed_model.get_text_embedding(node.get_content(metadata_mode="all"))
        node.embedding = node_embedding

    vector_store.add(nodes=nodes)
