import logging
import sys

from settings import Constants


class LoggerFactory:
    def __init__(
        self,
        log_level: str | int = Constants.LOGGER_LOG_LEVEL,
        log_to_console: bool = Constants.LOGGER_LOG_TO_CONSOLE,
        log_to_file: bool = Constants.LOGGER_LOG_TO_FILE,
        log_file_path: str = Constants.LOGGER_LOG_FILE_PATH,
        max_bytes: int = Constants.LOGGER_MAX_BYTES,
        backup_count: int = Constants.LOGGER_BACKUP_COUNT,
    ):
        self.log_level = log_level
        self.log_to_console = log_to_console
        self.log_to_file = log_to_file
        self.log_file_path = log_file_path
        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def get_logger(
        self,
        name: str,
    ) -> logging.Logger:
        """
        Get the logger instance
        """
        logger = logging.getLogger(name=name)
        logger.setLevel(self.log_level)

        if not logger.hasHandlers():
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            if self.log_to_console:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setLevel(self.log_level)
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            if self.log_to_file:
                file_handler = logging.handlers.RotatingFileHandler(
                    self.log_file_path,
                    maxBytes=self.max_bytes,
                    backupCount=self.backup_count,
                )
                file_handler.setLevel(self.log_level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        return logger
