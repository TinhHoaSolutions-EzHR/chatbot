from fastapi import APIRouter, status

from app.models.api import APIResponse
from app.utils.api_response import BackendAPIResponse

router = APIRouter(tags=["base"])


@router.get("/", response_model=APIResponse, status_code=status.HTTP_200_OK)
async def home():
    """
    Just a simple home endpoint to show the API's information
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


@router.get("/ping", response_model=APIResponse, status_code=status.HTTP_200_OK)
async def ping():
    """
    Just a simple ping endpoint to check if the API is running
    """
    return BackendAPIResponse().set_message("Pong!").respond()
