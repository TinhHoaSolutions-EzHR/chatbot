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
    POSTGRES_CONNECTOR_URI = (
        "postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    )

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


class Secrets:
    # LLM API Key
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    # Relational Database Credentials
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "root")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123")
    POSTGRES_NAME = os.getenv("POSTGRES_NAME", "ezhr_chatbot")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
