from app.exception.base_exceptions import BaseExceptionTest
from app.exception.utils.error_code import ErrorCodes


class InternalServerErrorException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.INTERNAL_SERVER_ERROR.value[1]
        super().__init__(error_code, *args)

class BadGatewayException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.BAD_GATEWAY.value[1]
        super().__init__(error_code, *args)

class ServiceUnavailableException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.SERVICE_UNAVAILABLE.value[1]
        super().__init__(error_code, *args)

class GatewayTimeoutException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.GATEWAY_TIMEOUT.value[1]
        super().__init__(error_code, *args)