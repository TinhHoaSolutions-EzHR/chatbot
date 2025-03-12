from app.exception.base_exceptions import BaseExceptionTest
from app.exception.utils.error_code import ErrorCodes

class ChatSessionNotFoundException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.CHAT_SESSION_NOT_FOUND.value[1]
        super().__init__(error_code, *args)

class ChatMessageNotFoundException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.CHAT_MESSAGE_NOT_FOUND.value[1]
        super().__init__(error_code, *args)

class LLMProviderNotFoundException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.LLM_PROVIDER_NOT_FOUND.value[1]
        super().__init__(error_code, *args)

class EmbeddingProviderNotFoundException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.EMBEDDING_PROVIDER_NOT_FOUND.value[1]
        super().__init__(error_code, *args)

class ProviderTypeChangeNotAllowedException(BaseExceptionTest):
    def __init__(self, *args):
        error_code = ErrorCodes.PROVIDER_TYPE_CHANGE_NOT_ALLOWED.value[1]
        super().__init__(error_code, *args)