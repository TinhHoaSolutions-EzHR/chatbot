from fastapi import APIRouter

from app.models.api import APIResponse
from app.utils.api_response import BackendAPIResponse

router = APIRouter(tags=["base"])


@router.get("/", response_model=APIResponse)
async def home():
    """
    Just a simple home endpoint to show the API's information
    """
    return (
        BackendAPIResponse()
        .set_data(
            {
                "org": "Tinh Hoa Solutions",
                "description": "API for LLM-based Application Chatbot",
            }
        )
        .respond()
    )


@router.get("/ping", response_model=APIResponse)
async def ping():
    """
    Just a simple ping endpoint to check if the API is running
    """
    return BackendAPIResponse().set_message("Pong!").respond()
