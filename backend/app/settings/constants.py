import logging
import os
from enum import auto
from enum import Enum


class Constants:
    PROJECT_NAME = "chatbot"

    # API Configuration
    FASTAPI_NAME = "EzHR Chatbot"
    FASTAPI_VERSION = os.getenv("API_VERSION", "1")
    FASTAPI_DESCRIPTION = "This is an API for the LLM-based assistant chatbot"
    FASTAPI_PREFIX = "/api/v1"

    # Relational Database Connection Configuration
    MSSQL_POOL_SIZE = 10
    MSSQL_MAX_OVERFLOW = 20
    MSSQL_POOL_TIMEOUT = 30
    MSSQL_POOL_RECYCLE = 3600
    MSSQL_DRIVER = "ODBC+Driver+17+for+SQL+Server"
    MSSQL_CONNECTOR_URI = "mssql+pyodbc://{user}:{password}@{host}:{port}/{db_name}?driver={driver}&TrustServerCertificate=yes"
    MSSQL_ASYNC_CONNECTOR_URI = "mssql+aioodbc://{user}:{password}@{host}:{port}/{db_name}?driver={driver}&TrustServerCertificate=yes"

    # Error Handler
    API_SUCCESS = "Success"
    INVALID_REQUEST_MESSAGE = "Invalid request"
    UNAUTHORIZED_REQUEST_MESSAGE = "Unauthorized request"
    FORBIDDEN_REQUEST_MESSAGE = "Forbidden request"
    NOT_FOUND_MESSAGE = "Not found"
    USER_NOT_FOUND_MESSAGE = "User not found"
    INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error"
    EMPTY_CHAT_MESSAGE_MESSAGE = "Empty chat message"

    # Logger Configuration
    LOGGER_LOG_LEVEL = os.getenv("LOGGER_LOG_LEVEL", logging.INFO)
    LOGGER_LOG_TO_CONSOLE = os.getenv("LOGGER_LOG_TO_CONSOLE", True)
    LOGGER_LOG_TO_FILE = os.getenv("LOGGER_LOG_TO_FILE", False)
    LOGGER_LOG_FILE_PATH = os.getenv("LOGGER_LOG_FILE_PATH", f"/var/log/{PROJECT_NAME}.log")
    LOGGER_MAX_BYTES = 10 * 1024 * 1024
    LOGGER_BACKUP_COUNT = 5

    # Seeding Configuration
    SEED_CONFIG_DIR = os.getenv("SEED_CONFIG_DIR", "/app/data/seeds")
    SEED_ON_STARTUP = os.getenv("SEED_ON_STARTUP", False)

    # Minio Configuration
    MINIO_DOCUMENT_BUCKET = os.getenv("MINIO_DOCUMENT_BUCKET", "documents")
    MINIO_IMAGE_BUCKET = os.getenv("MINIO_IMAGE_BUCKET", "images")

    # Redis Configuration
    REDIS_SCHEME = "redis"
    REDIS_DB_NUM = 0
    REDIS_MAX_CONNECTIONS = 10
    REDIS_DB_NUMBER_CELERY = int(os.environ.get("REDIS_DB_NUMBER_CELERY", 15))
    REDIS_DB_NUMBER_CELERY_RESULT_BACKEND = int(
        os.environ.get("REDIS_DB_NUMBER_CELERY_RESULT_BACKEND", 14)
    )
    REDIS_HEALTH_CHECK_INTERVAL = int(os.environ.get("REDIS_HEALTH_CHECK_INTERVAL", 60))

    # Llama Index Configuration
    # NOTE: the EMBEDDING_BATCH_SIZE is 50, and LLM_MAX_OUTPUT_LENGTH is 512
    # should be small under development, to reduce costs
    RETRY_TIMES = 3
    LLM_REDIS_CACHE_COLLECTION = "ezhr_chatbot_cache"
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    INGESTION_BATCH_SIZE = 32
    EMBEDDING_BATCH_SIZE = 50
    DIMENSIONS = 1536
    DISTANCE_METRIC_TYPE = "Cosine"
    LLM_MAX_OUTPUT_LENGTH = 512
    LLM_MAX_CONTEXT_WINDOW = 128_000  # max context window of gpt-4o-mini
    QDRANT_COLLECTION = "ezhr_chatbot"
    SIMILARITY_TOP_K = 5

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

    # Chat Message
    MAX_USER_MESSAGE_LENGTH = 2000

    # Identicon Configuration
    AGENT_AVATAR_IDENTICON_FOREGROUND_COLOR = ["#d73027", "#f46d43", "#fdae61", "#fee08b"]
    AGENT_AVATAR_IDENTICON_BACKGROUND_COLOR = "rgb(224,224,224)"
    AGENT_AVATAR_IDENTICON_WIDTH = 200
    AGENT_AVATAR_IDENTICON_HEIGHT = 200
    AGENT_AVATAR_IDENTICON_OUTPUT_FORMAT = "png"
    # User Settings
    MAX_RECENT_AGENTS = 5

    # OAuth
    GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

    # JWT
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 3600))
    EZHR_ACCESS_TOKEN = "ezhr_access_token"

    # Celery
    RUN_INDEXING = "run_indexing"
    CELERY_BROKER_POOL_LIMIT = int(os.environ.get("CELERY_BROKER_POOL_LIMIT", 10))
    CELERY_SEPARATOR = ":"
    CELERY_RESULT_EXPIRES = int(os.environ.get("CELERY_RESULT_EXPIRES", 86400))
    CELERY_WORKER_CONCURRENCY = 4
    CELERY_WORKER_POOL = "threads"
    CELERY_WORKER_PREFETCH_MULTIPLIER = 1

    # Datetime Format
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    # Document
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

    # LLM Prompts
    CHAT_SESSION_NAMING_PROMPT = """
    Generate a short and concise title (5-10 words) for the chat session based on the following conversation:

    User: {user_message}
    Agent: {agent_message}

    Provide answer without double quotes.
    """

    CHAT_ENGINE_SYSTEM_PROMPT = """
    You are a human resources professional at a company that needs to quickly find information in its policy documents.

    Guidelines:
    - Provide information explicitly stated in policy documents
    - For basic contextual questions (company name, policy type, etc), use ONLY information directly visible in the provided context
    - No assumptions or interpretations about policy details
    - Do not explain
    - Your primary language is Vietnamese
    - If you cannot find an answer, please output "Không tìm thấy thông tin, hãy liên hệ HR. SĐT: 0919 397 169 (Ms. Nhã) hoặc email hr@giaiphaptinhhoa.com"
    - If the response is empty, please answer with the knowledge you have

    Let's work this out in a step by step way to be sure we have the right answer.
    Answer as the tone of a human resources professional, be polite and helpful."""

    CHAT_ENGINE_CONTEXT_PROMPT = """
    The following is a friendly conversation between an employee and a human resources professional.
    The professional is talkative and provides lots of specific details from her context.
    If the professional does not know the answer to a question, she truthfully says she does not know.

    Here are the relevant documents for the context:
    '''
    {context_str}
    '''

    ## Instruction
    Based on the above documents, provide a detailed answer for the employee question below.
    Answer "don't know" if not present in the document."""

    CHAT_ENGINE_CONTEXT_REFINE_PROMPT = """
    The following is a friendly conversation between an employee and a human resources professional.
    The professional is talkative and provides lots of specific details from her context.
    If the professional does not know the answer to a question, she truthfully says she does not know.

    Here are the relevant documents for the context:
    '''
    {context_msg}
    '''

    Existing Answer:
    '''
    {existing_answer}
    '''

    ## Instruction
    Refine the existing answer using the provided context to assist the user.
    If the context isn't helpful, just repeat the existing answer and nothing more."""

    CHAT_ENGINE_CONDENSE_PROMPT = """
    Given the following conversation between an employee and a human resources professional and a follow up question from the employee.
    Your task is to firstly summarize the chat history and secondly condense the follow up question into a standalone question.

    Chat History:
    '''
    {chat_history}
    '''

    Follow Up Input:
    '''
    {question}
    '''

    Output format: a standalone question.

    Your response:"""


class CeleryPriority(int, Enum):
    HIGHEST = 0
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()
    LOWEST = auto()
