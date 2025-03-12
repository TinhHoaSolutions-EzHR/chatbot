

class ExceptionConstants:
    # Auth errors
    AUTHENTICATION_FAILED = "Authentication failed. Please check your credentials."
    UNAUTHORIZED_REQUEST = "The request requires user authentication information."
    ACCESS_DENIED = "Access denied. You do not have permission to perform this action."
    TOKEN_EXPIRED = "Your authentication token has expired."
    TOKEN_INVALID = "The provided authentication token is invalid."
    REFRESH_TOKEN_EXPIRED = "Your refresh token has expired. Please log in again."
    USER_NOT_FOUND = "User with email {0} not found."
    USER_ALREADY_EXISTS = "A user with the given email already exists."
    PERMISSION_DENIED = "You do not have the necessary permissions to perform this action."
    OAUTH_LOGIN_FAILED = "OAuth login failed. Please try again."

    # Request errors
    BAD_REQUEST = "Bad request."
    INVALID_REQUEST = "The server could not understand the request due to incorrect syntax."
    INVALID_QUERY_PARAMETER = "Invalid query parameter: {0}."
    FORBIDDEN_REQUEST = "Unauthorized request. The client does not have access rights to the content.",
    NOT_FOUND = "The requested resource was not found."
    REQUEST_TIMEOUT = "The server timed out waiting for the request."
    DUPLICATE_REQUEST = "Duplicate request detected. Please wait before trying again."
    NOT_ACCEPTABLE = "The requested resource is not acceptable according to the Accept header."
    PAYLOAD_TOO_LARGE = "The request payload is too large."
    UNSUPPORTED_MEDIA_TYPE = "The request media type is unsupported."
    RANGE_NOT_SATISFIABLE = "The requested range is not satisfiable."
    TOO_MANY_REQUESTS = "The client has sent too many requests in a short period."

    # Database errors
    DB_OPERATION_FAILED = "A general database operational error occurred."
    DB_DEADLOCK_DETECTED = "A database deadlock was detected and the transaction was aborted."

    # MSSQL errors
    MSSQL_OPERATION_FAILED = "A general operational error occurred in MSSQL."
    MSSQL_QUERY_FAILED = "An error occurred while executing the SQL query."

    # Redis errors
    REDIS_KEY_NOT_FOUND = "The requested Redis key was not found."
    REDIS_CONNECTION_FAILED = "Failed to connect to Redis."
    REDIS_TIMEOUT = "Redis request timed out."

    # MinIO errors
    MINIO_BUCKET_NOT_FOUND = "The specified MinIO bucket does not exist."
    MINIO_CONNECTION_FAILED = "Failed to establish a connection with MinIO."
    MINIO_UPLOAD_FAILED = "An error occurred while uploading a file to MinIO."
    MINIO_DOWNLOAD_FAILED = "An error occurred while downloading a file from MinIO."

    # Chatbot errors
    CHAT_SESSION_NOT_FOUND = "Chat session not found."
    CHAT_MESSAGE_NOT_FOUND = "Chat message not found."
    LLM_PROVIDER_NOT_FOUND = "LLM provider not found."
    EMBEDDING_PROVIDER_NOT_FOUND = "Embedding provider not found."
    PROVIDER_TYPE_CHANGE_NOT_ALLOWED = "Provider type change not allowed."

    # Server errors
    INTERNAL_SERVER_ERROR = "An internal server error occurred."
    BAD_GATEWAY = "The server received an invalid response."
    SERVICE_UNAVAILABLE = "The server is temporarily unavailable. Please try again later."
    GATEWAY_TIMEOUT = "The server is experiencing high load. Please try again shortly."



