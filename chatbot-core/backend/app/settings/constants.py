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
    LOGGER_LOG_TO_CONSOLE = True
    LOGGER_LOG_TO_FILE = False
    LOGGER_LOG_FILE_PATH = "api.log"
    LOGGER_MAX_BYTES = 10485760
    LOGGER_BACKUP_COUNT = 5

    # Minio Configuration
    MINIO_DOCUMENT_BUCKET = os.getenv("MINIO_DOCUMENT_BUCKET", "documents")
    MINIO_IMAGE_BUCKET = os.getenv("MINIO_IMAGE_BUCKET", "images")

    # Redis Configuration
    REDIS_DB_NUM = 0
    REDIS_MAX_CONNECTIONS = 10

    # Llama Index Configuration
    # NOTE: the EMBEDDING_BATCH_SIZE is 50, and LLM_MAX_OUTPUT_LENGTH is 512
    # should be small under development, to reduce costs
    RETRY_TIMES = 3
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
