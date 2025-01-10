from datetime import datetime
from typing import Any
from typing import List
from typing import Optional

from fastapi import UploadFile
from llama_index.core import Settings
from llama_index.core.extractors import KeywordExtractor
from llama_index.core.extractors import QuestionsAnsweredExtractor
from llama_index.core.extractors import SummaryExtractor
from llama_index.core.ingestion import IngestionCache
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.vector_stores.qdrant import QdrantVectorStore

from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.settings import Constants
from app.utils.api.helpers import parse_pdf


def get_transformations() -> List[Any]:
    """
    Get the transformation components for the ingestion pipeline.

    Returns:
        List[Any]: List of LlamaIndex transformation components
    """
    # Define node postprocessor methods
    extractors = [
        SummaryExtractor(llm=Settings.llm, summaries=["prev", "self"]),
        QuestionsAnsweredExtractor(llm=Settings.llm, questions=2),
        KeywordExtractor(llm=Settings.llm, keywords=5),
    ]

    # Define chunking method
    splitter = HierarchicalNodeParser.from_defaults(chunk_sizes=[512, 128])

    # Define full transformation pipeline
    transformations = [splitter, *extractors, Settings.embed_model]

    return transformations


def index_document_to_vector_db(
    document: UploadFile,
    issue_date: datetime = datetime.now(),
    is_outdated: bool = False,
    qdrant_connector: Optional[QdrantConnector] = None,
    redis_connector: Optional[RedisConnector] = None,
) -> None:
    """
    Index a PDF document into the vector database.

    Args:
        uploaded_document (UploadFile): Document to be indexed.
        issue_date (datetime): Issue date of the document. Defaults to the current date.
        is_outdated (bool): Flag to indicate if the document is outdated. Defaults to False.
        qdrant_connector (Optional[QdrantConnector]): Qdrant connector. Defaults to None.
        redis_connector (Optional[RedisConnector]): Redis connector. Defaults to None.
    """
    # Parse PDF file into LlamaIndex Document objects
    documents = parse_pdf(document=document, issue_date=issue_date, is_outdated=is_outdated)

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
        vector_store=vector_store,
        cache=ingest_cache,
        # TODO: Remove this parameter after finishing the development
        disable_cache=True,
    )
    pipeline.run(documents=documents, show_progress=True, batch_size=Constants.INGESTION_BATCH_SIZE)

    # TODO: Will be deleted after figuring out why vector embeddings
    # are not being stored in the Qdrant database when calling IngestionPipeline.run()
    # for node in nodes:
    #     node_embedding = Settings.embed_model.get_text_embedding(
    #         node.get_content(metadata_mode="all")
    #     )
    #     node.embedding = node_embedding

    # vector_store.add(nodes=nodes)
