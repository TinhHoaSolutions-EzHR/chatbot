import time
from typing import Any

from celery.exceptions import WorkerShutdown
from redis.exceptions import RedisError

from app.background.helpers import ProbeConfig
from app.background.helpers import timeout_context
from app.databases.mssql import get_db_session
from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.utils.api.error_handler import RedisProbeError
from app.utils.api.helpers import get_logger


logger = get_logger(__name__)


def wait_for_redis(sender: Any, **kwargs) -> None:
    """
    Wait for Redis to be available before starting the Celery worker.
    Will raise WorkerShutdown to kill the celery worker if the timeout is reached.

    Args:
        sender (Any): The sender of the signal.
        **kwargs: Arbitrary keyword arguments.
    """
    probe_config = ProbeConfig()
    redis_client = RedisConnector().client

    logger.info("Redis: Readiness probe starting")

    try:
        with timeout_context() as get_elapsed:
            while True:
                # Check if the Redis server is ready
                try:
                    if redis_client.ping():
                        logger.info("Redis: Readiness probe succeeded")
                        break
                except RedisError as e:
                    logger.warning(f"Redis: Ping failed: {e}")

                # Check if the timeout is reached
                elapsed = get_elapsed()
                if elapsed > probe_config.wait_limit:
                    logger.error(
                        f"Redis: Readiness probe did not succeed within the timeout "
                        f"({probe_config.wait_limit} seconds). Exiting..."
                    )
                    raise WorkerShutdown("Redis: Readiness probe timeout")

                logger.info(
                    f"Redis: Readiness probe ongoing. elapsed={elapsed:.1f} timeout={probe_config.wait_limit:.1f}"
                )
                time.sleep(probe_config.wait_interval)
    except Exception as e:
        if not isinstance(e, WorkerShutdown):
            logger.error(f"Redis: Unexpected error during readiness probe: {e}")
            raise RedisProbeError(f"Probe failed with error: {e}") from e
        raise


def wait_for_db(sender: Any, **kwargs) -> None:
    """
    Wait for the database to be available before starting the Celery worker.
    Will raise WorkerShutdown to kill the celery worker if the timeout is reached.

    Args:
        sender (Any): The sender of the signal.
        **kwargs: Arbitrary keyword arguments.
    """
    probe_config = ProbeConfig()

    try:
        with timeout_context() as get_elapsed:
            while True:
                # Check if the database server is ready
                try:
                    with get_db_session() as session:
                        session.execute("SELECT 1")
                        logger.info("Database: Readiness probe succeeded")
                        break
                except Exception as e:
                    logger.warning(f"Database: Probe failed: {e}")

                # Check if the timeout is reached
                elapsed = get_elapsed()
                if elapsed > probe_config.wait_limit:
                    logger.error(
                        f"Database: Readiness probe did not succeed within the timeout "
                        f"({probe_config.wait_limit} seconds). Exiting..."
                    )
                    raise WorkerShutdown("Database: Readiness probe timeout")

                logger.info(
                    f"Database: Readiness probe ongoing. elapsed={elapsed:.1f} timeout={probe_config.wait_limit:.1f}"
                )
                time.sleep(probe_config.wait_interval)
    except Exception as e:
        if not isinstance(e, WorkerShutdown):
            logger.error(f"Database: Unexpected error during readiness probe: {e}")
            raise RedisProbeError(f"Probe failed with error: {e}") from e
        raise


def wait_for_qdrant(sender: Any, **kwargs) -> None:
    """
    Wait for Qdrant to be available before starting the Celery worker.
    Will raise WorkerShutdown to kill the celery worker if the timeout is reached.
    """
    probe_config = ProbeConfig()
    qdrant_connector = QdrantConnector()

    try:
        with timeout_context() as get_elapsed:
            while True:
                # Check if the Qdrant server is ready
                try:
                    if qdrant_connector.health_check():
                        logger.info("Qdrant: Readiness probe succeeded")
                        break
                except Exception as e:
                    logger.warning(f"Qdrant: Probe failed: {e}")

                # Check if the timeout is reached
                elapsed = get_elapsed()
                if elapsed > probe_config.wait_limit:
                    logger.error(
                        f"Qdrant: Readiness probe did not succeed within the timeout "
                        f"({probe_config.wait_limit} seconds). Exiting..."
                    )
                    raise WorkerShutdown("Qdrant: Readiness probe timeout")

                logger.info(
                    f"Qdrant: Readiness probe ongoing. elapsed={elapsed:.1f} timeout={probe_config.wait_limit:.1f}"
                )
                time.sleep(probe_config.wait_interval)
    except Exception as e:
        if not isinstance(e, WorkerShutdown):
            logger.error(f"Qdrant: Unexpected error during readiness probe: {e}")
            raise RedisProbeError(f"Probe failed with error: {e}") from e
        raise
