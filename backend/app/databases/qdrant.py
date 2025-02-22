import requests
from fastapi import Request
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

from app.databases.base import BaseConnector
from app.settings import Constants
from app.settings import Secrets
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


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
            logger.error(f"Error initializing vector database: {e}", exc_info=True)

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
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )

    def health_check(self) -> bool:
        """
        Check the health status of the vector database

        Returns:
            bool: True if the vector database is healthy, False otherwise
        """
        response = requests.get(f"http://{Secrets.QDRANT_HOST}:{Secrets.QDRANT_PORT}/healthz")
        if "healthz check passed" in response.text:
            return True

        return False


def get_qdrant_connector(request: Request) -> QdrantConnector:
    """
    Get the instance of the vector database connection

    Args:
        request (Request): FastAPI request object

    Returns:
        QdrantConnector: Vector database connection instance
    """
    return request.app.state.qdrant_conn
