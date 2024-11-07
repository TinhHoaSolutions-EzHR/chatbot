from typing import Optional, Any
from pydantic import BaseModel

from models.api import APIResponse, APIError
from utils.error_handler import handle_error
from settings import Constants


class BackendAPIResponse:
    def __init__(self) -> None:
        # Initialize the APIResponse object
        resp = APIResponse(
            status_code=200,
            message="Success",
        )

        self.resp = resp

    def set_status_code(self, status_code: int) -> "BackendAPIResponse":
        """
        Set the status code of the response
        """
        self.resp.status_code = status_code
        return self

    def set_message(self, message: str) -> "BackendAPIResponse":
        """
        Set the message of the response
        """
        self.resp.message = message
        return self

    def set_headers(self, headers: Optional[Any]) -> "BackendAPIResponse":
        """
        Set the headers of the response
        """
        self.resp.headers = headers
        return self

    def set_data(self, data: Optional[Any]) -> "BackendAPIResponse":
        """
        Set the data of the response
        """
        self.resp.data = data
        return self

    def respond(self) -> APIResponse:
        """
        Return the APIResponse object
        """
        return self.resp.model_dump()


def handle_api_response(
    data: Any,
    err: APIError,
    success_status_code: int,
    model_response: BaseModel | None = None,
) -> APIResponse:
    """
    Helper function to handle service responses and construct API responses
    """
    if err:
        status_code, message = handle_error(err=err)
    else:
        status_code, message = success_status_code, Constants.API_SUCCESS

    if data:
        data = (
            [model_response.model_validate(item) for item in data]
            if isinstance(data, list)
            else model_response.model_validate(data)
        )

    return (
        BackendAPIResponse()
        .set_status_code(status_code=status_code)
        .set_message(message=message)
        .set_data(data=data)
        .respond()
    )
