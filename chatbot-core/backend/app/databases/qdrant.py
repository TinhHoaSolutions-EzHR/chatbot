from qdrant_client import QdrantClient, models

from app.settings import Secrets
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class QdrantConnector:
    """
    Qdrant connector class

    Pattern: Singleton
    Purpose: Create a single instance of the vector database connection
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> QdrantClient:
        """
        Get the instance of the vector database connection
        """
        if cls._instance is None:
            cls._instance = cls()._create_qdrant_client()

        return cls._instance

    @classmethod
    def _create_qdrant_client(cls) -> QdrantClient | None:
        """
        Create the vector database connection if there is no any existing connection
        """
        try:
            return QdrantClient(host=Secrets.QDRANT_HOST, port=Secrets.QDRANT_PORT)
        except Exception as e:
            logger.error(f"Error initializing vector database: {e}")
            raise

    def _create_collection(
        self,
        collection_name: str,
        vector_size: int = 1536,
        distance: str = models.Distance.COSINE,
    ) -> None:
        """
        Create a collection in the vector database

        Args:
            collection_name (str): Collection name
            vector_size (int, optional): Vector size. Defaults to 1536.
            distance (str, optional): Distance metric. Defaults to "Cosine".
        """
        # Check if the collection exists
        is_exists = self._instance.collection_exists(collection_name=collection_name)
        if is_exists:
            return

        # Create a collection
        self._instance.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorsConfig(size=vector_size, distance=distance),
        )


def get_vector_db_client() -> QdrantClient:
    """
    Get the instance of the vector database connection
    """
    return QdrantConnector.get_instance()
