from collections.abc import Iterator

import pytest
from qdrant_client import QdrantClient
from tests.utils import validate_config

from app.settings import Constants
from app.settings import Secrets


@pytest.fixture
def qdrant_client() -> Iterator[QdrantClient]:
    """
    Create Qdrant client
    """
    # Validate the Qdrant connection configuration
    validate_config(o=Secrets, required=["QDRANT_HOST", "QDRANT_PORT"])

    # Create Qdrant client
    # TODO: Use HTTPS connection in production
    yield QdrantClient(host=Secrets.QDRANT_HOST, port=Secrets.QDRANT_PORT, https=False)


def test_qdrant_connection(qdrant_client: QdrantClient) -> None:
    """
    Test Qdrant connection
    """
    try:
        # Check if the server is accessible by listing collections
        collections = qdrant_client.get_collections()
        assert collections is not None, "Expected to list collections, but got None."
    except Exception as e:
        pytest.fail(f"Unexpected error while connecting to Qdrant: {e}.")


def test_qdrant_create_collection(qdrant_client: QdrantClient) -> None:
    """
    Test Qdrant collection creation

    Args:
        qdrant_client (QdrantClient): Qdrant client
    """
    collection_name = Constants.QDRANT_TEST_COLLECTION

    try:
        # Attempt to create a new collection
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "size": Constants.QDRANT_DIMENSIONS,
                "distance": Constants.QDRANT_DISTANCE_METRIC_TYPE,
            },
        )

        # Check if the collection was created successfully
        collection = qdrant_client.collection_exists(collection_name=collection_name)
        assert (
            collection is True
        ), f"Expected collection '{collection_name}' to be created, but it was not."
    except Exception as e:
        pytest.fail(f"Unexpected error while creating Qdrant collection: {e}.")
    finally:
        # Delete the collection after the test
        qdrant_client.delete_collection(collection_name=collection_name)
