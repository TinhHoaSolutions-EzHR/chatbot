from typing import Any
from typing import Dict

from app.background.celery_worker import background_app
from app.databases.minio import MinioConnector
from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.integrations.llama_index.ingestion_pipelines import IndexingPipeline
from app.settings import Constants
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


@background_app.task(name=Constants.RUN_INDEXING)
def run_indexing(
    file_path: str,
    metadata: Dict[str, Any] = {},
) -> None:
    """
    Run indexing task to embed documents into vector database.

    Args:
        file_path (str): Path to the document file to be indexed.
        metadata (Dict[str, Any]): Metadata for the embedding vector.
    """
    minio_connector = MinioConnector()
    qdrant_connector = QdrantConnector()
    redis_connector = RedisConnector()

    logger.info(f"Indexing task for document {file_path} started.")

    # Get the document from the object storage
    document = minio_connector.get_file(
        object_name=file_path,
        bucket_name=Constants.MINIO_DOCUMENT_BUCKET,
    )
    if document is None:
        logger.error(f"Failed to retrieve document {file_path} from Minio.")
        return

    # Run the indexing pipeline to embed the document into the vector database
    indexing_pipeline = IndexingPipeline(
        qdrant_connector=qdrant_connector,
        redis_connector=redis_connector,
    )
    indexing_pipeline.run(document=document, metadata=metadata)

    # Log the task end
    logger.info(f"Indexing task for document {file_path} completed.")
