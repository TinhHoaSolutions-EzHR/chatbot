import contextlib
from qdrant_client import QdrantClient, models
from typing import Iterator

from app.databases.base import BaseConnector
from app.settings import Constants, Secrets
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class QdrantConnector(BaseConnector[QdrantClient]):
    """
    Qdrant connector class

    Pattern: Singleton
    Purpose: Create a single instance of the vector database connection
    """

    _o = Secrets
    _required_keys = ["QDRANT_HOST", "QDRANT_PORT"]

    @classmethod
    def _create_client(cls) -> QdrantClient | None:
        """
        Create the vector database connection if there is no any existing connection

        Returns:
            QdrantClient | None: Vector database connection instance
        """
        try:
            return QdrantClient(host=Secrets.QDRANT_HOST, port=Secrets.QDRANT_PORT)
        except Exception as e:
            logger.error(f"Error initializing vector database: {e}")
            raise

    def create_collection(
        self,
        collection_name: str,
        vector_size: int = Constants.DIMENSIONS,
        distance: str = Constants.DISTANCE_METRIC_TYPE,
    ) -> None:
        """
        Create a collection in the vector database

        Args:
            collection_name (str): Collection name
            vector_size (int, optional): Vector size. Defaults to 1536.
            distance (str, optional): Distance metric. Defaults to "Cosine".
        """
        # Check if the collection exists
        is_exists = self._client.collection_exists(collection_name=collection_name)
        if is_exists:
            return

        # Create a collection
        self._client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorsConfig(size=vector_size, distance=distance),
        )


@contextlib.contextmanager
def get_vector_db_connector() -> Iterator[QdrantConnector]:
    """
    Get the instance of the vector database connection

    Yield:
        QdrantConnector: Vector database connection instance
    """
    qdrant_connector = QdrantConnector()
    yield qdrant_connector