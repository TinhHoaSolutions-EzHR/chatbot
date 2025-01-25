from typing import Any

from celery import Celery
from celery.signals import setup_logging
from celery.signals import worker_init
from celery.signals import worker_ready
from celery.signals import worker_shutdown

import app.background.utils as utils
from app.utils.api.helpers import get_logger


logger = get_logger(__name__)


# Initialize Celery
app = Celery(__name__)
app.config_from_object("app.background.configs.base")


@worker_init.connect
def on_worker_init(sender: Any, **kwargs) -> None:
    """
    Initialize the Celery worker

    Args:
        sender (Any): The sender of the signal.
        **kwargs: Arbitrary keyword arguments.
    """
    logger.info("Worker initialization started")

    # Wait for the services to be ready
    utils.wait_for_redis(sender=sender, **kwargs)
    utils.wait_for_db(sender=sender, **kwargs)
    utils.wait_for_qdrant(sender=sender, **kwargs)


@worker_ready.connect
def on_worker_ready(sender: Any = None, **kwargs) -> None:
    """
    Handles worker ready signal. This runs when the worker is ready to process tasks,
    after initialization is complete.

    Args:
        sender (Any): The sender of the signal.
        **kwargs: Arbitrary keyword arguments.
    """
    utils.on_worker_ready(sender=sender, **kwargs)


@worker_shutdown.connect
def on_worker_shutdown(sender: Any = None, **kwargs) -> None:
    """
    Handles worker shutdown signal. This runs when the worker is shutting down.

    Args:
        sender (Any): The sender of the signal.
        **kwargs: Arbitrary keyword arguments.
    """
    utils.on_worker_shutdown(sender=sender, **kwargs)


@setup_logging.connect
def on_setup_logging(loglevel: Any, logfile: Any, format: Any, colorize: Any, **kwargs) -> None:
    """
    Setup logging for the Celery worker.

    Args:
        loglevel (Any): The logging level.
        logfile (Any): The file to log to.
        format (Any): The log format.
        colorize (Any): Whether to colorize the log.
        **kwargs: Additional keyword arguments.
    """
    utils.on_setup_logging(
        loglevel=loglevel,
        logfile=logfile,
        format=format,
        colorize=colorize,
        **kwargs,
    )


# Auto-discover tasks
app.autodiscover_tasks(["app.background.tasks.indexing"])
