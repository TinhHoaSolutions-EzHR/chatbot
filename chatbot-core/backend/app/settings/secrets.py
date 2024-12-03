import os


class Secrets:
    # LLM API Key
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    # Relational Database Credentials
    MSSQL_HOST = os.getenv("MSSQL_HOST", "127.0.0.1")
    MSSQL_USER = os.getenv("MSSQL_USER", "SA")
    MSSQL_SA_PASSWORD = os.getenv("MSSQL_SA_PASSWORD", "P&ssword123")
    MSSQL_DB = os.getenv("MSSQL_DB", "chatbot_core")

    # Minio Credentials
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "127.0.0.1:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "S3User")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "P&ssword123")

    # Qdrant Credentials
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

    # Redis Credentials
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
