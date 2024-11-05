from backend.models.api import APIResponse
from typing import Optional, Any

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
    
    def set_pagination(self, pagination: Optional[Any]) -> "BackendAPIResponse":
        """
        Set the pagination of the response
        """
        self.resp.pagination = pagination
        return self
    
    def respond(self) -> APIResponse:
        """
        Return the APIResponse object
        """
        return self.resp.model_dump()