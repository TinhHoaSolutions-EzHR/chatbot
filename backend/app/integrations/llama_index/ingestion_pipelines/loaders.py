from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from fastapi import UploadFile
from llama_index.core import Settings
from llama_index.core.extractors import KeywordExtractor
from llama_index.core.ingestion import IngestionCache
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.vector_stores.qdrant import QdrantVectorStore

from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.settings import Constants
from app.utils.api.helpers import parse_pdf


class IndexingPipeline:
    def __init__(
        self,
        qdrant_connector: Optional[QdrantConnector] = None,
        redis_connector: Optional[RedisConnector] = None,
    ):
        """
        Initialize the indexing pipeline that indexes a PDF document into the vector database.
        We utilize some concepts of LlamaIndex like node post-processors, chunking and the ingestion pipeline.

        Args:
            qdrant_connector (Optional[QdrantConnector]): Qdrant connector. Defaults to None.
            redis_connector (Optional[RedisConnector]): Redis connector. Defaults to None.
        """
        self._qdrant_connector = qdrant_connector
        self._redis_connector = redis_connector

    @staticmethod
    def _get_transformations() -> List[Any]:
        """
        Get the transformation components for the ingestion pipeline.

        Returns:
            List[Any]: List of LlamaIndex transformation components
        """
        # Define node postprocessor methods
        extractors = [
            # SummaryExtractor(llm=Settings.llm, summaries=["prev", "self"]),
            # QuestionsAnsweredExtractor(llm=Settings.llm, questions=2),
            KeywordExtractor(llm=Settings.llm, keywords=5),
        ]

        # Define chunking method
        splitter = HierarchicalNodeParser.from_defaults(chunk_sizes=[512, 128])

        # Define full transformation pipeline
        transformations = [splitter, *extractors, Settings.embed_model]

        return transformations

    def run(self, document: UploadFile, metadata: Dict[str, Any] = {}):
        """
        Run the indexing pipeline.

        Args:
            document (UploadFile): Document to be indexed.
            metadata (Dict[str, Any]): Additional metadata for the document. Defaults to {}.
        """
        # Parse PDF file into LlamaIndex Document objects
        documents = parse_pdf(document=document, metadata=metadata)

        # Create a collection in the vector database
        self._qdrant_connector.create_collection(
            collection_name=Constants.LLM_QDRANT_COLLECTION,
        )

        # Initialize the vector store for the ingestion pipeline
        qdrant_client = self._qdrant_connector.client
        vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name=Constants.LLM_QDRANT_COLLECTION,
        )

        # Initialize the cache store for the ingestion pipeline
        redis_cache = self._redis_connector.get_cache_store()
        ingest_cache = IngestionCache(
            cache=redis_cache,
            collection=Constants.LLM_REDIS_CACHE_COLLECTION,
        )

        # Define transformation components (chunking + node post-processors)
        transformations = self._get_transformations()

        # Ingestion pipeline to vector database
        pipeline = IngestionPipeline(
            name="EzHR Chatbot Indexing Pipeline",
            transformations=transformations,
            vector_store=vector_store,
            cache=ingest_cache,
            # TODO: Remove this parameter after finishing the development
            disable_cache=True,
        )
        pipeline.run(
            documents=documents, show_progress=True, batch_size=Constants.INGESTION_BATCH_SIZE
        )
