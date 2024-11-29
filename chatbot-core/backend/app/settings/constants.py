import os
import logging


class Constants:
    # API Configuration
    FASTAPI_NAME = "EzHR Chatbot"
    FASTAPI_VERSION = "1.0.0"
    FASTAPI_DESCRIPTION = ("This is an API for the LLM-based assistant chatbot",)
    FASTAPI_PREFIX = "/api/v1"

    # LLM API URL
    LLM_API_URL = os.getenv("LLM_API_URL")

    # Relational Database Connection Configuration
    POSTGRES_POOL_SIZE = 10
    POSTGRES_MAX_OVERFLOW = 20
    POSTGRES_POOL_TIMEOUT = 30
    POSTGRES_POOL_RECYCLE = 3600
    POSTGRES_CONNECTOR_URI = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

    # Error Handler
    API_SUCCESS = "Success"
    INVALID_REQUEST_MESSAGE = "Invalid request"
    UNAUTHORIZED_REQUEST_MESSAGE = "Unauthorized request"
    FORBIDDEN_REQUEST_MESSAGE = "Forbidden request"
    NOT_FOUND_MESSAGE = "Not found"
    INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error"

    # Logger Configuration
    LOGGER_LOG_LEVEL = logging.INFO
    LOGGER_LOG_TO_CONSOLE = True
    LOGGER_LOG_TO_FILE = False
    LOGGER_LOG_FILE_PATH = "api.log"
    LOGGER_MAX_BYTES = 10485760
    LOGGER_BACKUP_COUNT = 5
