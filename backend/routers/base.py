from fastapi import APIRouter
import http

from utils.create_api_response import BackendAPIResponse

router = APIRouter(prefix="/", tags=["base"])


@router.get("/", response_model=BackendAPIResponse)
async def home():
    """
    Just a simple home endpoint to show the API's information
    """
    return (
        BackendAPIResponse()
        .set_status_code(http.HTTPStatus.OK)
        .set_data(
            {
                "org": "Tinh Hoa Solutions",
                "description": "API for LLM-based Application Chatbot",
            }
        )
        .respond()
    )


@router.get("/ping", response_model=BackendAPIResponse)
async def ping():
    """
    Just a simple ping endpoint to check if the API is running
    """
    return (
        BackendAPIResponse()
        .set_status_code(http.HTTPStatus.OK)
        .set_message("Pong!")
        .respond()
    )
