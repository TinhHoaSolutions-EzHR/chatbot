from app.exception.utils.message_utils import MessageUtils


class BaseExceptionTest(Exception):
    def __init__(self, error_code: str, *args):
        self.error_code = error_code
        self.detail = MessageUtils.get_message(error_code, *args)
        super().__init__(f"{self.error_code}: {self.detail}")

    def __str__(self):
        return f"{self.error_code}: {self.detail}"
