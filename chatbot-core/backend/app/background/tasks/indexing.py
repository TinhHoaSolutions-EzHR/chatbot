import time

from app.background.celery_worker import app
from app.settings import Constants
from app.utils.api.helpers import get_logger


logger = get_logger(__name__)


@app.task(name=Constants.RUN_INDEXING)
def run_indexing() -> None:
    """
    Run indexing task.
    """
    # Log the task start
    logger.info("Indexing task started.")

    # Simulate indexing process
    for i in range(10):
        logger.info(f"Indexing progress: {i * 10}%")
        time.sleep(2)

    # Log the task end
    logger.info("Indexing task completed.")
