import logging
import os


class Constants:
    PROJECT_NAME = "chatbot-core"

    # API Configuration
    FASTAPI_NAME = "EzHR Chatbot"
    FASTAPI_VERSION = "1.0.0"
    FASTAPI_DESCRIPTION = ("This is an API for the LLM-based assistant chatbot",)
    FASTAPI_PREFIX = "/api/v1"

    # Relational Database Connection Configuration
    MSSQL_POOL_SIZE = 10
    MSSQL_MAX_OVERFLOW = 20
    MSSQL_POOL_TIMEOUT = 30
    MSSQL_POOL_RECYCLE = 3600
    MSSQL_CONNECTOR_URI = (
        "mssql+pyodbc://{user}:{password}@{host}:{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
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

    # Minio Configuration
    MINIO_DOCUMENT_BUCKET = os.getenv("MINIO_DOCUMENT_BUCKET", "documents")

    # Redis Configuration
    REDIS_DB_NUM = 0
    REDIS_MAX_CONNECTIONS = 10

    # Llama Index Configuration
    LLM_QDRANT_COLLECTION = "ezhr_chatbot"
    LLM_REDIS_CACHE_COLLECTION = "ezhr_chatbot_cache"
    OPENAI_LLM_MODEL = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
    INGESTION_BATCH_SIZE = 32
