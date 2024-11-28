import os


class Secrets:
    # LLM API Key
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    # Relational Database Credentials
    MSSQL_HOST = os.getenv("MSSQL_HOST", "localhost")
    MSSQL_USER = os.getenv("MSSQL_USER", "SA")
    MSSQL_SA_PASSWORD = os.getenv("MSSQL_SA_PASSWORD", "password")
    MSSQL_DB_NAME = os.getenv("MSSQL_DB_NAME", "ezhr_chatbot")
    MSSQL_PORT = int(os.getenv("MSSQL_PORT", 1433))

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
