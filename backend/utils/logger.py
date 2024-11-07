import logging
import sys


class LoggerFactory:
    def __init__(
        self,
        log_level: str | int = logging.INFO,
        log_to_console: bool = True,
        log_to_file: bool = False,
        log_file_path: str = "api.log",
        max_bytes: int = 10485760,
        backup_count: int = 5,
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
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

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
