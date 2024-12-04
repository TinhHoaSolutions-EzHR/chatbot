from typing import Annotated
from typing import Any
from typing import List

from fastapi import File
from fastapi import UploadFile
from llama_index.core import Settings
from llama_index.core.extractors import KeywordExtractor
from llama_index.core.extractors import QuestionsAnsweredExtractor
from llama_index.core.ingestion import IngestionCache
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import BaseNode
from llama_index.vector_stores.qdrant import QdrantVectorStore

from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.settings import Constants
from app.utils.pdf_reader import parse_pdf


def get_transformations() -> List[Any]:
    """
    Get the transformation components for the ingestion pipeline

    Returns:
        List[Any]: List of LlamaIndex transformation components
    """
    # TODO: Add two fields `issue_date` (datetime) and `outdated` (bool) to the document metadata

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
    document: Annotated[UploadFile, File(description="PDF file")],
    qdrant_connector: QdrantConnector,
    redis_connector: RedisConnector,
) -> None:
    """
    Index a PDF document into the vector database.

    Args:
        document (UploadFile): PDF file
        qdrant_connector (QdrantConnector): Vector database connection
        redis_connector (RedisConnector): Cache store connection
    """
    # Parse PDF file into LlamaIndex Document objects
    documents = parse_pdf(document=document)

    # Create a collection in the vector database
    qdrant_connector.create_collection(
        collection_name=Constants.LLM_QDRANT_COLLECTION,
    )

    # Initialize the vector store for the ingestion pipeline
    qdrant_client = qdrant_connector.client
    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=Constants.LLM_QDRANT_COLLECTION,
    )

    # Initialize the cache store for the ingestion pipeline
    redis_cache = redis_connector.get_cache_store()
    ingest_cache = IngestionCache(
        cache=redis_cache,
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
