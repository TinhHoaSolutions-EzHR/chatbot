import asyncio
import logging.handlers
import os
import sys
from collections.abc import Callable
from datetime import datetime
from typing import Annotated
from typing import List
from typing import Optional
from typing import Type

import pdfplumber
import yaml
from celery import current_task
from fastapi import File
from fastapi import Request
from fastapi import UploadFile
from llama_index.core import Document

from app.settings import Constants
from app.settings import Secrets
from app.utils.api.error_handler import PdfParsingError

# TODO: Replace this logger by own logger after moving logger logic to separate module
logger = logging.getLogger(__name__)


def remove_vietnamese_accents(input_str: str) -> str:
    """
    Remove Vietnamese accents from a string.

    Args:
        input_str (str): Input string with accents.

    Returns:
        str: Output string without accents.
    """
    S1 = "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ"
    S0 = "AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy"

    return "".join([S0[S1.index(c)] if c in S1 else c for c in input_str])


def parse_pdf(
    document: Annotated[UploadFile, File(description="PDF file")],
) -> List[Document] | None:
    """
    Parse a PDF file into Llamaindex Document objects.

    Args:
        document (UploadFile): PDF file to parse.

    Returns:
        List[Document]: List of Llamaindex Document objects.
    """
    try:
        documents = []
        with pdfplumber.open(document.file) as pdf:
            for page in pdf.pages:
                documents.append(Document(text=page.extract_text()))
    except Exception as e:
        raise PdfParsingError(message="Error parsing PDF", detail=str(e))

    return documents


# TODO: Separate the logger configuration into a separate module
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[1;31m",  # Bold Red
        "NOTSET": "\033[91m",  # Reset
        "NOTICE": "\033[94m",  # Blue
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record when logging to the console.

        Args:
            record (logging.LogRecord): Log record.

        Returns:
            str: Formatted log message.
        """
        levelname = record.levelname
        if levelname in self.COLORS:
            prefix = self.COLORS[levelname]
            suffix = "\033[0m"

            formatted_message = super().format(record)
            level_display = f"{prefix}{levelname}{suffix}:"
            return f"{level_display.ljust(4)} {formatted_message}"

        return super().format(record)


class PlainFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record when logging to a file.

        Args:
            record (logging.LogRecord): Log record.

        Returns:
            str: Formatted log message.
        """
        levelname = record.levelname
        level_display = f"{levelname}:"
        formatted_message = super().format(record)
        return f"{level_display.ljust(4)} {formatted_message}"


class CeleryTaskColoredFormatter(ColoredFormatter):
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record of a Celery task when logging to the console.

        Args:
            record (logging.LogRecord): Log record.

        Returns:
            str: Formatted log message.
        """
        task = current_task
        if task and task.request:
            record.__dict__.update(task_id=task.request.id, task_name=task.name)
            record.msg = f"[{task.name}({task.request.id})] {record.msg}"

        return super().format(record)


class CeleryTaskPlainFormatter(PlainFormatter):
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record of a Celery task when logging to a file.

        Args:
            record (logging.LogRecord): Log record.

        Returns:
            str: Formatted log message.
        """
        task = current_task
        if task and getattr(task, "request", None):
            record.__dict__.update(task_id=task.request.id, task_name=task.name)
            record.msg = f"[{task.name}({task.request.id})] {record.msg}"

        return super().format(record)


def setup_logging_handler(
    logger: logging.Logger,
    handler: logging.Handler,
    formatter: logging.Formatter,
    log_level: str | int,
    include_uvicorn: bool = True,
    uvicorn_logger: Optional[logging.Logger] = None,
) -> None:
    """
    Set up a logging handler.

    Args:
        logger (logging.Logger): Logger instance.
        handler (logging.Handler): Logging handler.
        formatter (logging.Formatter): Logging formatter.
        log_level (str | int): Log level.
        log_file_path (str): Log file path. Defaults to None.
        include_uvicorn (bool): Include Uvicorn logs. Defaults to True.
        uvicorn_logger (logging.Logger): Uvicorn logger. Defaults to None.
    """
    # Set the log level and formatter for the handler
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # If Uvicorn logs should be included, configure the Uvicorn logger.
    if include_uvicorn and uvicorn_logger:
        uvicorn_logger.addHandler(handler)


def get_logger(
    name: Optional[str] = None,
    from_logger: Optional[logging.Logger] = None,
    log_level: str | int = Constants.LOGGER_LOG_LEVEL,
    log_to_console: bool = Constants.LOGGER_LOG_TO_CONSOLE,
    log_to_file: bool = Constants.LOGGER_LOG_TO_FILE,
    log_file_path: str = Constants.LOGGER_LOG_FILE_PATH,
    max_bytes: int = Constants.LOGGER_MAX_BYTES,
    backup_count: int = Constants.LOGGER_BACKUP_COUNT,
    console_formatter: Type[logging.Formatter] = ColoredFormatter,
    file_formatter: Type[logging.Formatter] = PlainFormatter,
    include_uvicorn: bool = True,
) -> logging.Logger:
    """
    Get a logger instance with optional console and file handlers.

    Args:
        name (str): Name of the logger.
        from_logger (logging.Logger): Existing logger instance to inherit from. Defaults to None.
        log_level (str | int): Log level. Defaults to INFO.
        log_to_console (bool): Log to console. Defaults to True.
        log_to_file (bool): Log to file. Defaults to False.
        log_file_path (str): Log file path. Defaults to /var/log/{PROJECT_NAME}.log.
        max_bytes (int): Max bytes. Defaults to 10MB.
        backup_count (int): Backup count. Defaults to 5.
        console_formatter (logging.Formatter): Console formatter. Defaults to ColoredFormatter.
        file_formatter (logging.Formatter): File formatter. Defaults to PlainFormatter.
        include_uvicorn (bool): Include uvicorn logs. Defaults to True.

    Returns:
        logging.Logger: Logger instance.
    """
    # Get the logger instance either from the existing logger or create a new one.
    logger: logging.Logger = None
    if not from_logger:
        name = name or __name__
        logger = logging.getLogger(name=name)
        logger.setLevel(log_level)
    else:
        logger = from_logger

    # If Uvicorn logs should be included, configure the Uvicorn logger.
    if include_uvicorn:
        uvicorn_logger = logging.getLogger("uvicorn.access")
        uvicorn_logger.handlers = []
        uvicorn_logger.setLevel(log_level)

    # Check if the logger already has handlers configured.
    if not logger.hasHandlers():
        # Set up a console handler.
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            setup_logging_handler(
                logger=logger,
                handler=console_handler,
                formatter=console_formatter(
                    fmt="%(asctime)s %(filename)30s %(lineno)4s: %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p",
                ),
                log_level=log_level,
                include_uvicorn=include_uvicorn,
                uvicorn_logger=uvicorn_logger,
            )

        # Set up a file handler.
        if log_to_file and log_file_path:
            # Verify the log file path exists
            verify_path_exists(path=os.path.dirname(log_file_path), create=True)

            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file_path, maxBytes=max_bytes, backupCount=backup_count
            )
            setup_logging_handler(
                logger=logger,
                handler=file_handler,
                formatter=file_formatter(
                    "%(asctime)s %(filename)30s %(lineno)4s: %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p",
                ),
                log_level=log_level,
                include_uvicorn=include_uvicorn,
                uvicorn_logger=uvicorn_logger,
            )

    return logger


def verify_path_exists(path: str, create: bool = False) -> None:
    """
    Verify if a path exists.

    Args:
        path (str): Path to verify.
        create (bool): Create the path if it does not exist. Defaults to False.
    """
    path_exists = os.path.exists(path)
    if not path_exists and create:
        try:
            os.makedirs(path)
            return
        except OSError as e:
            raise OSError(f"Failed to create directory '{path}'") from e

    raise FileNotFoundError(f"Directory '{path}' does not exist")


def construct_file_path(object_name: str, user_id: str = None) -> str:
    """
    Construct file path in Minio.

    Args:
        object_name (str): Name of the object.
        user_id (str): User id. Defaults to None.

    Returns:
        str: File path in Minio.

    Example:
        >>> construct_file_path("avatar", "user_id")
        # my_avatar_f6f7b43c-c0ca-4003-8143-7c5e767cde12_20211013123456.png
    """
    file_name = (
        (remove_vietnamese_accents(input_str=object_name).replace(" ", "_").lower())
        + "_"
        + user_id
        + "_"
        + datetime.now().strftime("%Y%m%d%H%M%S")
        + "."
        + Constants.AGENT_AVATAR_IDENTICON_OUTPUT_FORMAT
    )
    file_path = os.path.join(Constants.MINIO_IMAGE_BUCKET, file_name)

    return file_path


def get_database_url() -> str:
    """
    Get the database URL.

    Returns:
        str: Database URL.

    Example:
        >>> get_database_url()
        'mssql+pyodbc://sa:password@localhost/db_name?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # Try create the database URL from the environment variables
        database_url = Constants.MSSQL_CONNECTOR_URI.format(
            user=Secrets.MSSQL_USER,
            password=Secrets.MSSQL_SA_PASSWORD,
            host=Secrets.MSSQL_HOST,
            port=Secrets.MSSQL_PORT,
            db_name=Secrets.MSSQL_DB,
            driver=Constants.MSSQL_DRIVER,
        )

    return database_url


def check_client_disconnected(request: Request) -> Callable[[], bool]:
    """
    Check if the client is disconnected when streaming response.

    Args:
        request (Request): Request object.

    Returns:
        Callable[[], bool]: Function to check if the client is disconnected.
    """

    async def is_client_disconnected() -> bool:
        try:
            return await request.is_disconnected()
        except asyncio.TimeoutError:
            logger.warning("Timeout error while checking if the client is disconnected")
            return True
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while checking if the client is disconnected: {str(e)}"
            )
            return True

    return is_client_disconnected


def load_yaml(file_path: str) -> dict:
    """
    Load a YAML file.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Loaded YAML file.
    """
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
