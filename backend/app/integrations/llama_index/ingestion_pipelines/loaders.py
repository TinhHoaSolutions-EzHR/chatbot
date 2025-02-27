import asyncio
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from llama_index.core import Settings
from llama_index.core.extractors import KeywordExtractor
from llama_index.core.extractors import SummaryExtractor
from llama_index.core.ingestion import IngestionCache
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import Node
from llama_index.vector_stores.qdrant import QdrantVectorStore

from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.integrations.llama_index.ingestion_pipelines.translators import Translator
from app.settings import Constants
from app.utils.api.helpers import get_logger
from app.utils.api.helpers import parse_pdf

logger = get_logger(__name__)


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
        semantic_splitter = SemanticSplitterNodeParser.from_defaults(
            embed_model=Settings.embed_model, breakpoint_percentile_threshold=85, buffer_size=3
        )

        # Define node postprocessor methods
        extractors = [
            KeywordExtractor(keywords=3),
            SummaryExtractor(summaries=["prev", "self", "next"]),
        ]

        transformations = [semantic_splitter, *extractors, Settings.embed_model]
        return transformations

    def _get_ingestion_pipeline(self) -> IngestionPipeline:
        """
        Get the ingestion pipeline for the indexing process.

        Returns:
            IngestionPipeline: LlamaIndex ingestion pipeline
        """
        # Initialize the vector store for the ingestion pipeline
        qdrant_client = self._qdrant_connector.client
        vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name=Constants.QDRANT_COLLECTION,
        )

        # Initialize the cache store for the ingestion pipeline
        redis_cache = self._redis_connector.get_cache_store()
        ingest_cache = IngestionCache(
            cache=redis_cache,
            collection=Constants.LLM_REDIS_CACHE_COLLECTION,
        )

        # Define transformation components (chunking + metadata extraction + embedding)
        transformations = self._get_transformations()
        pipeline = IngestionPipeline(
            name="EzHR Chatbot Indexing Pipeline",
            transformations=transformations,
            vector_store=vector_store,
            cache=ingest_cache,
            # TODO: Remove this parameter after finishing the development
            disable_cache=True,
        )

        return pipeline

    def run(self, document: bytes, metadata: Dict[str, Any] = {}) -> List[Node]:
        """
        Run the indexing pipeline.

        Args:
            document (bytes): Document to be indexed.
            metadata (Dict[str, Any]): Additional metadata for the document. Defaults to {}.
        """
        try:
            # Parse PDF file into LlamaIndex Document objects
            logger.info("Parsing PDF document into LlamaIndex Document objects")
            documents = parse_pdf(document=document, metadata=metadata)

            # Initialize the translator and translate the document
            # logger.info("Translating the document into Vietnamese")
            # translator = Translator.from_defaults(
            #     source_language="english", target_language="vietnamese"
            # )
            # translated_documents = translator.get_translated_documents(documents)

            logger.info("Running the indexing pipeline")
            pipeline = self._get_ingestion_pipeline()
            nodes = pipeline.run(
                documents=documents,
                show_progress=True,
                batch_size=Constants.INGESTION_BATCH_SIZE,
            )
            return nodes
        except Exception:
            logger.error("Failed to run indexing pipeline for document", exc_info=True)

    def arun(self, document: bytes, metadata: Dict[str, Any] = {}):
        """
        Run the indexing pipeline.

        Args:
            document (bytes): Document to be indexed.
            metadata (Dict[str, Any]): Additional metadata for the document. Defaults to {}.
        """
        try:
            # Parse PDF file into LlamaIndex Document objects
            documents = parse_pdf(document=document, metadata=metadata)

            # Initialize the translator and translate the document
            translator = Translator.from_defaults(
                source_language="english", target_language="vietnamese"
            )
            translated_documents = translator.get_translated_documents(documents)

            pipeline = self._get_ingestion_pipeline()
            nodes = asyncio.run(
                pipeline.arun(
                    documents=translated_documents,
                    show_progress=True,
                    batch_size=Constants.INGESTION_BATCH_SIZE,
                )
            )
            return nodes
        except Exception:
            logger.error("Failed to run indexing pipeline for document", exc_info=True)
