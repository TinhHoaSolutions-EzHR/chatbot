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


class Secrets:
    # LLM API Key
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    # Relational Database Credentials
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "root")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123")
    POSTGRES_NAME = os.getenv("POSTGRES_NAME", "ezhr_chatbot")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

    # Minio Credentials
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

    # Qdrant Credentials
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

    # Redis Credentials
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
