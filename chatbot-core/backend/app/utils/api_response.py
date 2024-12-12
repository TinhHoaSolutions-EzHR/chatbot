from typing import Any
from typing import Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    message: str = "Success"
    headers: Optional[Any] = None
    data: Optional[Any] = None


class APIError(BaseModel):
    kind: Any


class BackendAPIResponse:
    def __init__(self) -> None:
        """
        The BackendAPIResponse class for handling API responses
        """
        # Initialize the APIResponse object
        resp = APIResponse(
            status_code=200,
            message="Success",
        )

        self.resp = resp

    def set_message(self, message: str) -> "BackendAPIResponse":
        """
        Set the message of the response

        Args:
            message (str): Message to be returned in the response

        Returns:
            BackendAPIResponse: The BackendAPIResponse object
        """
        self.resp.message = message
        return self

    def set_headers(self, headers: Optional[Any]) -> "BackendAPIResponse":
        """
        Set the headers of the response

        Args:
            headers (Optional[Any]): Headers to be returned in the response

        Returns:
            BackendAPIResponse: The BackendAPIResponse object
        """
        self.resp.headers = headers
        return self

    def set_data(self, data: Optional[Any]) -> "BackendAPIResponse":
        """
        Set the data of the response

        Args:
            data (Optional[Any]): Data to be returned in the response

        Returns:
            BackendAPIResponse: The BackendAPIResponse object
        """
        self.resp.data = data
        return self

    def respond(self) -> APIResponse:
        """
        Return the APIResponse object

        Returns:
            APIResponse: The APIResponse object
        """
        return self.resp.model_dump()
