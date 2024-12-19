from fastapi import APIRouter
from fastapi import status

from app import __version__
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse

router = APIRouter(tags=["base"])


@router.get("/", response_model=APIResponse, status_code=status.HTTP_200_OK)
def home() -> BackendAPIResponse:
    """
    Just a simple home endpoint to show the API's information

    Returns:
        BackendAPIResponse: API response
    """
    return (
        BackendAPIResponse()
        .set_data(
            {
                "organization": "Tinh Hoa Solutions",
                "description": "API for LLM-based Application Chatbot",
            }
        )
        .respond()
    )


@router.get("/health", response_model=APIResponse, status_code=status.HTTP_200_OK)
def healthcheck() -> BackendAPIResponse:
    """
    Just a simple ping endpoint to check if the API is running

    Returns:
        BackendAPIResponse: API response
    """
    return BackendAPIResponse().set_message("ok!").respond()


@router.get("/version", response_model=APIResponse, status_code=status.HTTP_200_OK)
def version() -> BackendAPIResponse:
    """
    Just a simple endpoint to show the API's version

    Returns:
        BackendAPIResponse: API response
    """
    return BackendAPIResponse().set_data({"version": __version__}).respond()
