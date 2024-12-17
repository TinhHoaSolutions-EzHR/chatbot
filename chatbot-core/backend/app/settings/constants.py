import logging
import os


class Constants:
    PROJECT_NAME = "chatbot-core"

    # API Configuration
    FASTAPI_NAME = "EzHR Chatbot"
    FASTAPI_VERSION = os.getenv("API_VERSION", "1.0.0")
    FASTAPI_DESCRIPTION = ("This is an API for the LLM-based assistant chatbot",)
    FASTAPI_PREFIX = "/api/v1"

    # Relational Database Connection Configuration
    MSSQL_POOL_SIZE = 10
    MSSQL_MAX_OVERFLOW = 20
    MSSQL_POOL_TIMEOUT = 30
    MSSQL_POOL_RECYCLE = 3600
    MSSQL_DRIVER = "ODBC+Driver+17+for+SQL+Server"
    MSSQL_CONNECTOR_URI = "mssql+pyodbc://{user}:{password}@{host}/{db_name}?driver={driver}"

    # Error Handler
    API_SUCCESS = "Success"
    INVALID_REQUEST_MESSAGE = "Invalid request"
    UNAUTHORIZED_REQUEST_MESSAGE = "Unauthorized request"
    FORBIDDEN_REQUEST_MESSAGE = "Forbidden request"
    NOT_FOUND_MESSAGE = "Not found"
    INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error"
    EMPTY_CHAT_MESSAGE_MESSAGE = "Empty chat message"

    # Logger Configuration
    LOGGER_LOG_LEVEL = os.getenv("LOGGER_LOG_LEVEL", logging.INFO)
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
    # NOTE: the EMBEDDING_BATCH_SIZE is 50, and LLM_MAX_OUTPUT_LENGTH is 512
    # should be small under development, to reduce costs
    LLM_QDRANT_COLLECTION = "ezhr_chatbot"
    LLM_REDIS_CACHE_COLLECTION = "ezhr_chatbot_cache"
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    INGESTION_BATCH_SIZE = 32
    EMBEDDING_BATCH_SIZE = 50
    DIMENSIONS = 768
    DISTANCE_METRIC_TYPE = "Cosine"
    LLM_MAX_OUTPUT_LENGTH = 512
    LLM_MAX_CONTEXT_WINDOW = 128_000  # max context window of gpt-4o-mini

    # Unit Test
    MINIO_TEST_BUCKET = "test-bucket"
    MINIO_TEST_UPLOADED_OBJECT_NAME = "test.txt"
    MINIO_TEST_FILE_CONTENT = b"EzHR Chatbot is a chatbot application that leverages the power of RAG (Retrieval-Augmented Generation) technique."

    QDRANT_TEST_COLLECTION = "test-collection"
    QDRANT_DIMENSIONS = 128
    QDRANT_DISTANCE_METRIC_TYPE = "Cosine"

    REDIS_TEST_KEY = "test-key"
    REDIS_TEST_VALUE = "test-value"

    MSSQL_TEST_DB_NAME = "tempdb"
