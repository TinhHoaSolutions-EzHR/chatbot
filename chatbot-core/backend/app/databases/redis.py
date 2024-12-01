import contextlib
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache
from redis import ConnectionPool, Redis
from typing import Iterator

from app.databases.base import BaseConnector
from app.settings import Constants, Secrets
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class RedisConnector(BaseConnector[Redis]):
    """
    Redis connector class

    Pattern: Singleton
    Purpose: Create a single instance of the Redis connection
    """

    _o = Secrets
    _required_keys = ["REDIS_HOST", "REDIS_PORT"]

    @staticmethod
    def _create_connection_pool() -> ConnectionPool | None:
        """
        Create the Redis connection pool if there is no any existing connection pool

        Returns:
            ConnectionPool | None: Redis connection pool instance
        """
        try:
            return ConnectionPool(
                host=Secrets.REDIS_HOST,
                port=Secrets.REDIS_PORT,
                db=Constants.REDIS_DB_NUM,
                max_connections=Constants.REDIS_MAX_CONNECTIONS,
            )
        except Exception as e:
            logger.error(f"Error initializing Redis connection pool: {e}")
            raise

    @classmethod
    def _create_client(cls) -> Redis | None:
        """
        Create the Redis connection if there is no any existing connection

        Returns:
            Redis | None: Redis connection instance
        """
        try:
            connection_pool = cls._create_connection_pool()
            return Redis(connection_pool=connection_pool)
        except Exception as e:
            logger.error(f"Error initializing Redis connection: {e}")
            raise

    def get_cache_store(self) -> RedisCache:
        """
        Get the cache store instance

        Returns:
            RedisCache: Redis cache store instance
        """
        return RedisCache(redis_client=self.client)


@contextlib.contextmanager
def get_cache_connector() -> Iterator[RedisConnector]:
    """
    Get the cache connector instance

    Yields:
        Iterator[RedisConnector]: Redis cache connector instance
    """
    redis_connector = RedisConnector()
    yield redis_connector
