import os


class Secrets:
    # LLM API Key
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    # Relational Database Credentials - PostgreSQL
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "chatbot")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

    # Minio Credentials
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "127.0.0.1:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "S3User")
    MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "P&ssword123")

    # Qdrant Credentials
    QDRANT_HOST = os.getenv("QDRANT_HOST", "127.0.0.1")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

    # Redis Credentials
    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # Ferment API Key
    FERMENT_API_KEY = os.getenv("FERMENT_API_KEY", "S5U3ze4WtNZcKZKjoHngcPTGmp1XqLKwjTZ3iuvET28=")

    # Google Oauth Credentials
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET_KEY")
