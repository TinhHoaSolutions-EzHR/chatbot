from app.exception.base_exceptions import BaseExceptionTest
from app.exception.utils.error_code import ErrorCodes


class BadRequestException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.BAD_REQUEST.value[1]
        super().__init__(error_code, *args)

class InvalidRequestException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.INVALID_REQUEST.value[1]
        super().__init__(error_code, *args)

class InvalidQueryParameterException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.INVALID_QUERY_PARAMETER.value[1]
        super().__init__(error_code, *args)

class ForbiddenException(BaseExceptionTest):  # 403
    def __init__(self, *args):
        error_code = ErrorCodes.FORBIDDEN_REQUEST.value[1]
        super().__init__(error_code, *args)

class NotFoundException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.NOT_FOUND.value[1]
        super().__init__(error_code, *args)

class RequestTimeoutException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.REQUEST_TIMEOUT.value[1]
        super().__init__(error_code, *args)

class DuplicateRequestException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.DUPLICATE_REQUEST.value[1]
        super().__init__(error_code, *args)

class NotAcceptableException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.NOT_ACCEPTABLE.value[1]
        super().__init__(error_code, *args)

class PayloadTooLargeException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.PAYLOAD_TOO_LARGE.value[1]
        super().__init__(error_code, *args)

class UnsupportedMediaTypeException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.UNSUPPORTED_MEDIA_TYPE.value[1]
        super().__init__(error_code, *args)

class RangeNotSatisfiableException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.RANGE_NOT_SATISFIABLE.value[1]
        super().__init__(error_code, *args)

class TooManyRequestsException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.TOO_MANY_REQUESTS.value[1]
        super().__init__(error_code, *args)