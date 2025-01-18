import time
from typing import Any

from celery.exceptions import WorkerShutdown
from celery.utils.log import get_task_logger
from redis.exceptions import RedisError
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.background.helpers import ProbeConfig
from app.background.helpers import timeout_context
from app.databases.mssql import MSSQLConnector
from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.utils.api.error_handler import RedisProbeError
from app.utils.api.helpers import CeleryTaskColoredFormatter
from app.utils.api.helpers import CeleryTaskPlainFormatter
from app.utils.api.helpers import ColoredFormatter
from app.utils.api.helpers import get_logger
from app.utils.api.helpers import PlainFormatter


logger = get_logger(__name__)
task_logger = get_task_logger(__name__)


def wait_for_redis(sender: Any, **kwargs) -> None:  # NOSONAR
    """
    Wait for Redis to be available before starting the Celery worker.
    Will raise WorkerShutdown to kill the celery worker if the timeout is reached.

    Args:
        sender (Any): The sender of the signal.
        **kwargs (Any): Additional keyword arguments.
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


def wait_for_db(sender: Any, **kwargs: Any) -> None:  # NOSONAR
    """
    Wait for the database to be available before starting the Celery worker.
    Will raise WorkerShutdown to kill the celery worker if the timeout is reached.

    Args:
        sender (Any): The sender of the signal.
        **kwargs (Any): Additional keyword arguments.
    """
    probe_config = ProbeConfig()

    try:
        with timeout_context() as get_elapsed:
            while True:
                try:
                    # Check if the database server is ready
                    with Session(MSSQLConnector.get_engine()) as session:
                        result = session.execute(text("SELECT 1")).scalar()
                        if result:
                            logger.info("Database: Readiness probe succeeded")

                            # Close the session
                            session.close()
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


def wait_for_qdrant(sender: Any, **kwargs: Any) -> None:  # NOSONAR
    """
    Wait for Qdrant to be available before starting the Celery worker.
    Will raise WorkerShutdown to kill the celery worker if the timeout is reached.

    Args:
        sender (Any): The sender of the signal.
        **kwargs (Any): Additional keyword arguments.
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


def on_worker_ready(sender: Any, **kwargs: Any) -> None:  # NOSONAR
    """
    Handles worker ready signal. This runs when the worker is ready to process tasks,
    after initialization is complete.

    Args:
        sender (Any): The sender of the signal.
        **kwargs (Any): Additional keyword arguments.
    """
    task_logger.info("Worker is ready to process tasks")


def on_worker_shutdown(sender: Any, **kwargs: Any) -> None:  # NOSONAR
    """
    Handles worker shutdown signal. This runs when the worker is shutting down.

    Args:
        sender (Any): The sender of the signal.
        **kwargs (Any): Additional keyword arguments.
    """
    task_logger.info("Worker is shutting down")


def on_setup_logging(
    loglevel: Any,
    logfile: Any,
    format: Any,
    colorize: Any,
    **kwargs: Any,  # NOSONAR
) -> None:
    """
    Setup logging for the Celery worker.

    Args:
        loglevel (Any): The logging level.
        logfile (Any): The file to log to.
        format (Any): The log format.
        colorize (Any): Whether to colorize the log.
        **kwargs (Any): Additional keyword arguments.
    """
    # Configure the logging for the Celery logger
    get_logger(
        from_logger=logger,
        log_level=loglevel,
        log_to_file=True if logfile else False,
        log_file_path=logfile,
        console_formatter=ColoredFormatter,
        file_formatter=PlainFormatter,
        include_uvicorn=False,
    )

    # Configure the logging for the task logger
    get_logger(
        from_logger=task_logger,
        log_level=loglevel,
        log_to_file=True if logfile else False,
        log_file_path=logfile,
        console_formatter=CeleryTaskColoredFormatter,
        file_formatter=CeleryTaskPlainFormatter,
        include_uvicorn=False,
    )
