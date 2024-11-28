from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache
from redis import ConnectionPool, Redis

from app.settings import Constants, Secrets
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class RedisConnector:
    """
    Redis connector class

    Pattern: Singleton
    Purpose: Create a single instance of the Redis connection
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> Redis:
        """
        Get the instance of the Redis connection
        """
        if cls._instance is None:
            cls._instance = cls()._create_redis_client()

        return cls._instance

    @classmethod
    def _create_connection_pool(cls) -> ConnectionPool | None:
        """
        Create the Redis connection pool if there is no any existing connection pool
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
    def _create_redis_client(cls) -> Redis | None:
        """
        Create the Redis connection if there is no any existing connection
        """
        try:
            connection_pool = cls._create_connection_pool()
            return Redis(connection_pool=connection_pool)
        except Exception as e:
            logger.error(f"Error initializing Redis connection: {e}")
            raise


def get_cache_store_client() -> RedisCache:
    """
    Get the cache store instance
    """
    return RedisCache(redis_client=RedisConnector.get_instance())
