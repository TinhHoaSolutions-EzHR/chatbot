from typing import Any
from typing import Dict
from typing import Optional

from fastapi import UploadFile

from app.background.celery_worker import background_app
from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.integrations.llama_index.ingestion_pipelines import IndexingPipeline
from app.settings import Constants
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


@background_app.task(name=Constants.RUN_INDEXING)
def run_indexing(
    document: UploadFile,
    qdrant_connector: Optional[QdrantConnector] = None,
    redis_connector: Optional[RedisConnector] = None,
    metadata: Dict[str, Any] = {},
):
    """
    Run indexing task to embed documents into vector database.

    Args:
        document (UploadFile): Document file to be indexed.
        qdrant_connector (Optional[QdrantConnector]): Vector database connection. Defaults to None.
        redis_connector (Optional[RedisConnector]): Cache store connection. Defaults to None.
        metadata (Dict[str, Any]): Metadata for the embedding vector.
    """
    # Log the task start
    logger.info(f"Indexing task for document {document.filename} starting...")

    indexing_pipeline = IndexingPipeline(
        qdrant_connector=qdrant_connector,
        redis_connector=redis_connector,
    )
    indexing_pipeline.run(document=document, metadata=metadata)

    # Log the task end
    logger.info(f"Indexing task for document {document.filename} completed.")
