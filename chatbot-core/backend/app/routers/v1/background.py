from fastapi import APIRouter
from fastapi import status

from app.background.celery_worker import app
from app.background.tasks.indexing import run_indexing
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.helpers import get_logger


logger = get_logger(__name__)
router = APIRouter(prefix="/background/tasks", tags=["background", "tasks"])


@router.get("/{task_id}/status", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_task_status(task_id: str) -> BackendAPIResponse:
    """
    Get the status of a task by task id.

    Args:
        task_id (str): Task id

    Returns:
        BackendAPIResponse: Backend API response with the task status.
    """
    # Get task result
    task_result = app.AsyncResult(id=task_id)

    # Construct the response
    data = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
    }

    return (
        BackendAPIResponse()
        .set_message(message="Task status retrieved successfully.")
        .set_data(data=data)
        .respond()
    )


@router.post("", response_model=APIResponse, status_code=status.HTTP_202_ACCEPTED)
def run_indexing_task() -> BackendAPIResponse:
    """
    Run indexing task.

    Returns:
        BackendAPIResponse: Backend API response with the task id.
    """
    # Run indexing task
    task = run_indexing.delay()

    # Construct the response
    data = {"task_id": task.id}

    return (
        BackendAPIResponse()
        .set_message(message="Indexing task started successfully.")
        .set_data(data=data)
        .respond()
    )
