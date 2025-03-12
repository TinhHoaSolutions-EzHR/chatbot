from app.exception.base_exceptions import BaseExceptionTest
from app.exception.utils.error_code import ErrorCodes


class DatabaseOperationalException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.DB_OPERATIONAL_ERROR.value[1]
        super().__init__(error_code, *args)

class DatabaseDeadlockException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.DB_DEADLOCK_ERROR.value[1]
        super().__init__(error_code, *args)

class MSSQLOperationalException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.MSSQL_OPERATIONAL_ERROR.value[1]
        super().__init__(error_code, *args)

class MSSQLQueryException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.MSSQL_QUERY_ERROR.value[1]
        super().__init__(error_code, *args)

class RedisKeyNotFoundException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.REDIS_KEY_NOT_FOUND.value[1]
        super().__init__(error_code, *args)

class RedisConnectionException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.REDIS_CONNECTION_ERROR.value[1]
        super().__init__(error_code, *args)

class RedisTimeoutException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.REDIS_TIMEOUT_ERROR.value[1]
        super().__init__(error_code, *args)

class MinIOBucketNotFoundException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.MINIO_BUCKET_NOT_FOUND.value[1]
        super().__init__(error_code, *args)

class MinIOConnectionException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.MINIO_CONNECTION_ERROR.value[1]
        super().__init__(error_code, *args)

class MinIOUploadException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.MINIO_UPLOAD_ERROR.value[1]
        super().__init__(error_code, *args)

class MinIODownloadException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.MINIO_DOWNLOAD_ERROR.value[1]
        super().__init__(error_code, *args)