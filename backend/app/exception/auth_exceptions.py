from app.exception.base_exceptions import BaseExceptionTest
from app.exception.utils.error_code import ErrorCodes

class OAuthLoginFailedException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.OAUTH_LOGIN_FAILED.value[1]
        super().__init__(error_code=error_code, *args)

class TokenInvalidException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.TOKEN_INVALID.value[1]
        super().__init__(error_code=error_code, *args)

class AuthenticationFailedException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.AUTHENTICATION_FAILED.value[1]
        super().__init__(error_code=error_code, *args)

class UnauthorizedRequestException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.UNAUTHORIZED_REQUEST.value[1]
        super().__init__(error_code=error_code, *args)

class TokenExpiredException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.TOKEN_EXPIRED.value[1]
        super().__init__(error_code=error_code, *args)

class RefreshTokenExpiredException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.REFRESH_TOKEN_EXPIRED.value[1]
        super().__init__(error_code=error_code, *args)

class AccessDeniedException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.ACCESS_DENIED.value[1]
        super().__init__(error_code=error_code,*args)

class PermissionDeniedException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.PERMISSION_DENIED.value[1]
        super().__init__(error_code=error_code, *args)

class UserNotFoundException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.USER_NOT_FOUND.value[1]
        super().__init__(error_code=error_code,*args)

class UserAlreadyExistsException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.USER_ALREADY_EXISTS.value[1]
        super().__init__(error_code=error_code, *args)

