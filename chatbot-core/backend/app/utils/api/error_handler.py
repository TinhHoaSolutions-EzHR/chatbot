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
    STARTER_MESSAGE_NOT_FOUND = (404, "Starter message not found")
    FOLDER_NOT_FOUND = (404, "Folder not found")
    CONNECTOR_NOT_FOUND = (404, "Connector not found")
    CHAT_SESSION_NOT_FOUND = (404, "Chat session not found")
    CHAT_MESSAGE_NOT_FOUND = (404, "Chat message not found")
    UNABLE_TO_UPLOAD_FILE_TO_MINIO = (404, "Unable to upload file to Minio")
    UNABLE_TO_DELETE_FILE_FROM_MINIO = (404, "Unable to delete file from Minio")
    LLM_PROVIDER_NOT_FOUND = (404, "LLM provider not found")
    USER_SETTING_NOT_FOUND = (404, "User setting not found")
    EMBEDDING_PROVIDER_NOT_FOUND = (404, "Embedding provider not found")
    PROVIDER_TYPE_CHANGE_NOT_ALLOWED = (422, "Provider type change not allowed")

    NO_CONTENT = (404, "No content found")

    USER_WRONG_LOGIN_METHOD = (405, "User already exists with wrong login method")


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


class PdfParsingError(BaseException):
    """
    Custom exception class for handling PDF parsing errors
    """


class PydanticParsingError(BaseException):
    """
    Custom exception class for handling Pydantic parsing errors
    """
