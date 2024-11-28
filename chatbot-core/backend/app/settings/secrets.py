import os


class Secrets:
    # LLM API Key
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    # Relational Database Credentials
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "root")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123")
    POSTGRES_NAME = os.getenv("POSTGRES_NAME", "ezhr_chatbot")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
