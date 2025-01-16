from typing import Any

from celery import Celery
from celery.signals import worker_init

from app.background.utils import wait_for_db
from app.background.utils import wait_for_qdrant
from app.background.utils import wait_for_redis
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
    wait_for_redis(sender, **kwargs)
    wait_for_db(sender, **kwargs)
    wait_for_qdrant(sender, **kwargs)


# Auto-discover tasks
app.autodiscover_tasks(["app.background.tasks.indexing"])
