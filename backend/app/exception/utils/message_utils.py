from app.settings.exception_constants import ExceptionConstants


class MessageUtils:
    _messages = {
        # Auth errors
        "AUTHENTICATION_FAILED": ExceptionConstants.AUTHENTICATION_FAILED,
        "UNAUTHORIZED_REQUEST": ExceptionConstants.UNAUTHORIZED_REQUEST,
        "ACCESS_DENIED": ExceptionConstants.ACCESS_DENIED,
        "TOKEN_EXPIRED": ExceptionConstants.TOKEN_EXPIRED,
        "TOKEN_INVALID": ExceptionConstants.TOKEN_INVALID,
        "REFRESH_TOKEN_EXPIRED": ExceptionConstants.REFRESH_TOKEN_EXPIRED,
        "USER_NOT_FOUND": ExceptionConstants.USER_NOT_FOUND,
        "USER_ALREADY_EXISTS": ExceptionConstants.USER_ALREADY_EXISTS,
        "PERMISSION_DENIED": ExceptionConstants.PERMISSION_DENIED,
        "OAUTH_LOGIN_FAILED": ExceptionConstants.OAUTH_LOGIN_FAILED,

        # Request errors
        "BAD_REQUEST": ExceptionConstants.BAD_REQUEST,
        "INVALID_REQUEST": ExceptionConstants.INVALID_REQUEST,
        "INVALID_QUERY_PARAMETER": ExceptionConstants.INVALID_QUERY_PARAMETER,
        "FORBIDDEN_REQUEST": ExceptionConstants.FORBIDDEN_REQUEST,
        "NOT_FOUND": ExceptionConstants.NOT_FOUND,
        "REQUEST_TIMEOUT": ExceptionConstants.REQUEST_TIMEOUT,
        "DUPLICATE_REQUEST": ExceptionConstants.DUPLICATE_REQUEST,
        "NOT_ACCEPTABLE": ExceptionConstants.NOT_ACCEPTABLE,
        "PAYLOAD_TOO_LARGE": ExceptionConstants.PAYLOAD_TOO_LARGE,
        "UNSUPPORTED_MEDIA_TYPE": ExceptionConstants.UNSUPPORTED_MEDIA_TYPE,
        "RANGE_NOT_SATISFIABLE": ExceptionConstants.RANGE_NOT_SATISFIABLE,
        "TOO_MANY_REQUESTS": ExceptionConstants.TOO_MANY_REQUESTS,

        # Database errors
        "DB_OPERATION_FAILED": ExceptionConstants.DB_OPERATION_FAILED,
        "DB_DEADLOCK_DETECTED": ExceptionConstants.DB_DEADLOCK_DETECTED,

        # MSSQL errors
        "MSSQL_OPERATION_FAILED": ExceptionConstants.MSSQL_OPERATION_FAILED,
        "MSSQL_QUERY_FAILED": ExceptionConstants.MSSQL_QUERY_FAILED,

        # Redis errors
        "REDIS_KEY_NOT_FOUND": ExceptionConstants.REDIS_KEY_NOT_FOUND,
        "REDIS_CONNECTION_FAILED": ExceptionConstants.REDIS_CONNECTION_FAILED,
        "REDIS_TIMEOUT": ExceptionConstants.REDIS_TIMEOUT,

        # MinIO errors
        "MINIO_BUCKET_NOT_FOUND": ExceptionConstants.MINIO_BUCKET_NOT_FOUND,
        "MINIO_CONNECTION_FAILED": ExceptionConstants.MINIO_CONNECTION_FAILED,
        "MINIO_UPLOAD_ERROR": ExceptionConstants.MINIO_UPLOAD_FAILED,
        "MINIO_DOWNLOAD_ERROR": ExceptionConstants.MINIO_DOWNLOAD_FAILED,

        # Chatbot errors
        "CHAT_SESSION_NOT_FOUND": ExceptionConstants.CHAT_SESSION_NOT_FOUND,
        "CHAT_MESSAGE_NOT_FOUND": ExceptionConstants.CHAT_MESSAGE_NOT_FOUND,
        "LLM_PROVIDER_NOT_FOUND": ExceptionConstants.LLM_PROVIDER_NOT_FOUND,
        "EMBEDDING_PROVIDER_NOT_FOUND": ExceptionConstants.EMBEDDING_PROVIDER_NOT_FOUND,
        "PROVIDER_TYPE_CHANGE_NOT_ALLOWED": ExceptionConstants.PROVIDER_TYPE_CHANGE_NOT_ALLOWED,

        # Server errors
        "INTERNAL_SERVER_ERROR": ExceptionConstants.INTERNAL_SERVER_ERROR,
        "BAD_GATEWAY": ExceptionConstants.BAD_GATEWAY,
        "SERVICE_UNAVAILABLE": ExceptionConstants.SERVICE_UNAVAILABLE,
        "GATEWAY_TIMEOUT": ExceptionConstants.GATEWAY_TIMEOUT,
    }

    @classmethod
    def get_message(cls, error_code: str, *args) -> str:
        message = cls._messages.get(error_code, error_code)
        return message.format(*args) if args else message