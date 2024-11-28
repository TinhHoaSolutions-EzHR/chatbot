from typing import Optional, Any
from fastapi import status

from app.models.api import APIResponse


class BackendAPIResponse:
    def __init__(self) -> None:
        # Initialize the APIResponse object
        resp = APIResponse(
            status_code=200,
            message="Success",
        )

        self.resp = resp

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
