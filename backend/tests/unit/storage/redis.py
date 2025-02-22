from collections.abc import Iterator

import pytest
from redis import Redis
from redis.exceptions import ConnectionError

from app.settings import Constants
from app.settings import Secrets
from tests.utils import validate_config


@pytest.fixture
def redis_client() -> Iterator[Redis]:
    """
    Create Redis client
    """
    # Validate the Redis connection configuration
    validate_config(o=Secrets, required=["REDIS_HOST", "REDIS_PORT"])

    # Create Redis client
    yield Redis(host=Secrets.REDIS_HOST, port=Secrets.REDIS_PORT)


def test_redis_connectivity(redis_client: Redis) -> None:
    """
    Test Redis connectivity

    Args:
        redis_client (Redis): Redis client
    """
    try:
        # Perform a simple ping to check if the server is accessible
        assert redis_client.ping(), "Expected to connect to Redis, but failed."
    except ConnectionError as e:
        pytest.fail(f"Connection error while connecting to Redis: {e}.")
    except Exception as e:
        pytest.fail(f"Unexpecyted error while connecting to Redis: {e}.")


def test_redis_set_get(redis_client: Redis) -> None:
    """
    Test Redis set and get operations

    Args:
        redis_client (Redis): Redis client
    """
    key = Constants.REDIS_TEST_KEY
    value = Constants.REDIS_TEST_VALUE

    try:
        # Set a key-value pair
        redis_client.set(key, value)

        # Get the value by key
        retrieved_value = redis_client.get(name=key)
        assert (
            redis_client.get(key) == retrieved_value
        ), f"Expected to get {value}, but got {retrieved_value}."
    except ConnectionError as e:
        pytest.fail(f"Connection error while setting and getting from Redis: {e}.")
    except Exception as e:
        pytest.fail(f"Unexpected error while setting and getting from Redis: {e}.")
