import os


class Constants:
    # API Configuration
    API_NAME = "EzHR Chatbot"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "This is an API for the LLM-based assistant chatbot"
    API_PREFIX = "/api/v1"

    # LLM API URL
    LLM_API_URL = os.getenv("LLM_API_URL")

    # Relational Database Connection Configuration
    POOL_SIZE = 10
    MAX_OVERFLOW = 20
    POOL_TIMEOUT = 30
    POOL_RECYCLE = 3600

    # Error Handler
    API_SUCCESS = "Success"
    NOT_EXISTING_ERROR = "Not existing error code"


class Secrets:
    # LLM API Key
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    # Relational Database Credentials
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "root")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123")
    POSTGRES_NAME = os.getenv("POSTGRES_NAME", "ezhr_chatbot")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"
