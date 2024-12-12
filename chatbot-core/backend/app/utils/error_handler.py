from enum import Enum

from app.settings import Constants


class ErrorCodesMappingNumber(Enum):
    INVALID_REQUEST = (400, Constants.INVALID_REQUEST_MESSAGE)
    UNAUTHORIZED_REQUEST = (401, Constants.UNAUTHORIZED_REQUEST_MESSAGE)
    FORBIDDEN_REQUEST = (403, Constants.FORBIDDEN_REQUEST_MESSAGE)
    NOT_FOUND = (404, Constants.NOT_FOUND_MESSAGE)
    INTERNAL_SERVER_ERROR = (500, Constants.INTERNAL_SERVER_ERROR_MESSAGE)

    # TODO: Think about adding more error codes here
    AGENT_NOT_FOUND = (404, "Agent not specified or found for chat session")
    CHAT_MESSAGES_NOT_FOUND = (404, "Chat message not found")


class BaseException(Exception):
    """
    Custom exception class for handling errors
    """

    def __init__(self, message: str, detail: str = None):
        super().__init__(message)
        self._message = message
        self._detail = detail

    def __str__(self):
        if self._detail:
            return f"{self._message}: {self._detail}"
        return self._message


class DatabaseTransactionError(BaseException):
    """
    Custom exception class for handling database transaction errors
    """


class ConnectorError(BaseException):
    """
    Custom exception class for handling connector errors
    """


class ConversationError(BaseException):
    """
    Custom exception class for handling chat message errors
    """
