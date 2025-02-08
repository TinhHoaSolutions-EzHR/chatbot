import os


class Secrets:
    # LLM API Key
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    # Relational Database Credentials
    MSSQL_HOST = os.getenv("MSSQL_HOST", "127.0.0.1")
    MSSQL_USER = os.getenv("MSSQL_USER", "SA")
    MSSQL_SA_PASSWORD = os.getenv("MSSQL_SA_PASSWORD", "P&ssword123")
    MSSQL_DB = os.getenv("MSSQL_DB", "chatbot_core")
    MSSQL_PORT = int(os.getenv("MSSQL_PORT", 1433))

    # Minio Credentials
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "127.0.0.1:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "S3User")
    MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "P&ssword123")

    # Qdrant Credentials
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

    # Redis Credentials
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # Ferment API Key
    FERMENT_API_KEY = os.getenv("FERMENT_API_KEY", "S5U3ze4WtNZcKZKjoHngcPTGmp1XqLKwjTZ3iuvET28=")

    # Google Oauth Credentials
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET_KEY")
